def calculate_cnj_check_digit(seq_str, year_str, j_str, tr_str, oooo_str):
    seq = seq_str.zfill(7)
    year = year_str.zfill(4)
    j = j_str
    tr = tr_str.zfill(2)
    oooo = oooo_str.zfill(4)
    number_str = f"{seq}{year}{j}{tr}{oooo}00"
    num = int(number_str)
    mod = num % 97
    check = 98 - mod
    return check

# Search sequence numbers around 1261994 that give check digit 42 for 2026.8.13.0000
print("Searching for 7-digit sequence numbers around 1261994:")
for seq in range(1261000, 1263000):
    check = calculate_cnj_check_digit(str(seq), "2026", "8", "13", "0000")
    if check == 42:
        print(f"Sequence: {seq} -> CNJ: {seq}-42.2026.8.13.0000")

# What if sequence is 8-digits (like 12619945 or similar) and comarca is 0000?
# Wait, for 8-digit sequence, the formula concatenates NNNNNNNN
print("\nSearching for 8-digit sequence numbers around 12619945:")
for seq in range(12619900, 12620000):
    # If 8-digit sequence, it concatenated as is
    number_str = f"{seq}2026813000000"
    num = int(number_str)
    mod = num % 97
    check = 98 - mod
    if check == 42:
        print(f"Sequence: {seq} -> CNJ: {seq}-42.2026.8.13.0000")
