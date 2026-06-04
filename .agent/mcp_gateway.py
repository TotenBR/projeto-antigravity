import asyncio
import sys
import json
import os
import traceback

WORKSPACE = "/home/toten/projeto-antigravity"
AGENT_DIR = os.path.join(WORKSPACE, ".agent")
CATALOG_PATH = os.path.join(AGENT_DIR, "mcp_catalog.json")
ACTIVE_MCPS_PATH = os.path.join(AGENT_DIR, "active_mcps.json")
LOG_PATH = os.path.join(AGENT_DIR, "mcp_gateway.log")

# Setup logging
def log(message):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    except Exception:
        pass

class ChildMCPProxy:
    def __init__(self, mcp_id, command, args, env_vars):
        self.mcp_id = mcp_id
        self.command = command
        self.args = args
        self.env_vars = env_vars
        self.process = None
        self.tools = []
        self.pending_requests = {}
        self.next_request_id = 1000
        
    async def start(self):
        # Merge environment variables
        env = os.environ.copy()
        if self.env_vars:
            for k, v in self.env_vars.items():
                if v:  # Only set if value is not empty
                    env[k] = v
                    
        log(f"Starting child MCP '{self.mcp_id}': {self.command} {' '.join(self.args)}")
        try:
            self.process = await asyncio.create_subprocess_exec(
                self.command, *self.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
                env=env
            )
            # Start task to read child's stdout
            asyncio.create_task(self.read_stdout_loop())
            
            # Send initialize handshake
            init_id = self.get_new_id()
            future = asyncio.get_running_loop().create_future()
            self.pending_requests[init_id] = future
            
            init_req = {
                "jsonrpc": "2.0",
                "id": init_id,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "mcp-gateway-client", "version": "1.0.0"}
                }
            }
            await self.send_json(init_req)
            
            # Wait for response from child
            log(f"Waiting for initialize response from '{self.mcp_id}'...")
            await asyncio.wait_for(future, timeout=10.0)
            log(f"Child '{self.mcp_id}' initialized.")
            
            # Send initialized notification
            initialized_notif = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            await self.send_json(initialized_notif)
            return True
        except Exception as e:
            log(f"Failed to start child '{self.mcp_id}': {e}\n{traceback.format_exc()}")
            return False
            
    def get_new_id(self):
        self.next_request_id += 1
        return self.next_request_id

    async def send_json(self, obj):
        if self.process and self.process.stdin:
            line = json.dumps(obj) + "\n"
            self.process.stdin.write(line.encode("utf-8"))
            await self.process.stdin.drain()

    async def read_stdout_loop(self):
        try:
            while self.process and self.process.stdout:
                line = await self.process.stdout.readline()
                if not line:
                    break
                line_str = line.decode("utf-8").strip()
                if not line_str:
                    continue
                try:
                    msg = json.loads(line_str)
                    msg_id = msg.get("id")
                    if msg_id in self.pending_requests:
                        future = self.pending_requests.pop(msg_id)
                        if not future.done():
                            future.set_result(msg)
                except Exception as e:
                    log(f"Error parsing child '{self.mcp_id}' line: {e}")
        except Exception as e:
            log(f"Stdout loop exception for child '{self.mcp_id}': {e}")

    async def get_tools_list(self):
        req_id = self.get_new_id()
        future = asyncio.get_running_loop().create_future()
        self.pending_requests[req_id] = future
        
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/list"
        }
        await self.send_json(req)
        try:
            res = await asyncio.wait_for(future, timeout=5.0)
            result = res.get("result", {})
            self.tools = result.get("tools", [])
            log(f"Loaded {len(self.tools)} tools from '{self.mcp_id}'")
            return self.tools
        except Exception as e:
            log(f"Error listing tools for child '{self.mcp_id}': {e}")
            return []

    async def call_tool(self, name, arguments):
        req_id = self.get_new_id()
        future = asyncio.get_running_loop().create_future()
        self.pending_requests[req_id] = future
        
        req = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        await self.send_json(req)
        try:
            res = await asyncio.wait_for(future, timeout=120.0)  # Allow time for dynamic browser scraping
            return res
        except Exception as e:
            log(f"Error calling tool '{name}' on '{self.mcp_id}': {e}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Timeout or error calling tool: {e}"}
            }

    def close(self):
        try:
            if self.process:
                self.process.terminate()
                log(f"Terminated child MCP '{self.mcp_id}'")
        except Exception as e:
            log(f"Error terminating child '{self.mcp_id}': {e}")

class StdioProtocol(asyncio.Protocol):
    def __init__(self, gateway):
        self.gateway = gateway
        self.buffer = b""

    def data_received(self, data):
        self.buffer += data
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            line_str = line.decode("utf-8").strip()
            if line_str:
                asyncio.create_task(self.gateway.handle_client_line(line_str))

    def connection_lost(self, exc):
        log("Connection from main client lost. Exiting...")
        self.gateway.stop()

class MCPGateway:
    def __init__(self):
        self.children = {}
        self.tool_to_child = {}
        self.running = True
        
    async def init_children(self):
        # Load active ids
        active_ids = ["filesystem", "fetch"]  # Default fallback
        if os.path.exists(ACTIVE_MCPS_PATH):
            try:
                with open(ACTIVE_MCPS_PATH, "r", encoding="utf-8") as f:
                    active_ids = json.load(f)
            except Exception as e:
                log(f"Error reading active_mcps: {e}")
                
        catalog = []
        if os.path.exists(CATALOG_PATH):
            try:
                with open(CATALOG_PATH, "r", encoding="utf-8") as f:
                    catalog = json.load(f)
            except Exception as e:
                log(f"Error reading catalog: {e}")
                
        catalog_map = {item["id"]: item for item in catalog}
        
        # Start each active MCP
        for mcp_id in active_ids:
            if mcp_id in catalog_map:
                item = catalog_map[mcp_id]
                proxy = ChildMCPProxy(mcp_id, item["command"], item["args"], item.get("env", {}))
                success = await proxy.start()
                if success:
                    self.children[mcp_id] = proxy
            else:
                log(f"Active MCP '{mcp_id}' not found in catalog.")
                
    async def handle_client_line(self, line_str):
        log(f"Client request received: {line_str}")
        try:
            req = json.loads(line_str)
            req_id = req.get("id")
            method = req.get("method")
            
            # Handle notifications (no id)
            if req_id is None:
                if method == "notifications/initialized":
                    log("Client notified initialization completion.")
                return
                
            # Handle methods
            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "antigravity-mcp-gateway",
                            "version": "1.0.0"
                        }
                    }
                }
                await self.send_to_client(res)
                
            elif method == "tools/list":
                all_tools = []
                self.tool_to_child.clear()
                
                # Fetch tools from all active child proxies
                for mcp_id, child in self.children.items():
                    tools = await child.get_tools_list()
                    for tool in tools:
                        tool_name = tool.get("name")
                        all_tools.append(tool)
                        self.tool_to_child[tool_name] = child
                        
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": all_tools
                    }
                }
                await self.send_to_client(res)
                
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                child = self.tool_to_child.get(tool_name)
                if child:
                    child_res = await child.call_tool(tool_name, arguments)
                    child_res["id"] = req_id
                    await self.send_to_client(child_res)
                else:
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found or owned by any active MCP."
                        }
                    }
                    await self.send_to_client(res)
            else:
                # Mock empty result for other list methods so we don't crash
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                }
                await self.send_to_client(res)
                
        except Exception as e:
            log(f"Error handling client request: {e}\n{traceback.format_exc()}")

    async def send_to_client(self, obj):
        line = json.dumps(obj) + "\n"
        log(f"Sending response to client: {line.strip()}")
        sys.stdout.write(line)
        sys.stdout.flush()

    def stop(self):
        self.running = False
        for mcp_id, child in self.children.items():
            child.close()
        sys.exit(0)

async def main():
    # Clean previous log
    if os.path.exists(LOG_PATH):
        try:
            os.remove(LOG_PATH)
        except Exception:
            pass
            
    log("Initializing MCP Gateway...")
    gateway = MCPGateway()
    await gateway.init_children()
    
    # Listen to standard input
    loop = asyncio.get_running_loop()
    stdio_transport, stdio_protocol = await loop.connect_read_pipe(
        lambda: StdioProtocol(gateway),
        sys.stdin
    )
    
    # Stay running
    while gateway.running:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
