# Preferências de Desenvolvimento e Execução do Usuário

Este arquivo contém preferências e regras de comportamento personalizadas solicitadas pelo usuário para este projeto. Todo agente Antigravity deve ler e aplicar estas diretrizes durante a execução das tarefas.

## Diretrizes Gerais
1. **Abertura Automática de PDFs:**
   - Sempre que um script ou tarefa gerar um arquivo PDF de relatório final, execute um comando para abri-lo automaticamente na tela do usuário para leitura imediata.
   - Em sistemas Linux (como este), utilize o comando `xdg-open <caminho_do_pdf>` via terminal para abrir o leitor padrão do sistema operacional.
   - **Importante (Evitar fechamento precoce):** Para evitar que o visualizador de PDF feche automaticamente quando o script Python ou o processo do terminal do agente terminar, o processo de abertura deve ser desvinculado (detached) da sessão pai.
     - Em Python: Use `subprocess.Popen(..., start_new_session=True)`.
     - Em comandos Bash: Prefira usar `setsid xdg-open <pdf> &` ou `nohup xdg-open <pdf> >/dev/null 2>&1 &`.
   - Caso a execução de `xdg-open` em segundo plano falhe devido a restrições de sessão gráfica da sandbox, informe o link absoluto do arquivo markdown e do PDF no chat para que o usuário possa clicar e abrir diretamente.

2. **Abertura de Pastas de Downloads:**
   - Ao concluir o download de arquivos em lote (como relatórios de FIIs), execute `xdg-open <diretorio>` para abrir o gerenciador de arquivos na tela do usuário.
