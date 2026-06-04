# Search for valid comarcas where check digit is 42
# For sequence 1261994, year 2026, J=8, TR=13
valid_matches = []
for comarca in range(10000):
    comarca_str = f"{comarca:04d}"
    # Calculate check digit for NNNNNNN-DD.YYYY.J.TR.OOOO
    # seq = 1261994, year = 2026, j = 8, tr = 13, oooo = comarca_str
    # Number: 1261994 2026 8 13 comarca_str 00
    number_str = f"12619942026813{comarca_str}00"
    num = int(number_str)
    mod = num % 97
    check = 98 - mod
    if check == 42:
        valid_matches.append(("1261994", comarca_str))

# What if sequence is 12619945 (8 digits sequence)?
# Standard CNJ allows sequence to be up to 7 digits. But some systems use 8?
# Let's check if seq is 12619945, year 2026, j=8, tr=13
for comarca in range(10000):
    comarca_str = f"{comarca:04d}"
    number_str = f"126199452026813{comarca_str}00"
    num = int(number_str)
    mod = num % 97
    check = 98 - mod
    if check == 42:
        valid_matches.append(("12619945", comarca_str))

print("Found matches:")
for seq, comarca in valid_matches:
    print(f"Sequence: {seq}, Comarca: {comarca} -> CNJ: {seq}-42.2026.8.13.{comarca}")
