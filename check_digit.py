def calculate_cnj_check_digit(seq_str, year_str, j_str, tr_str, oooo_str):
    # Concatenate: NNNNNNN YYYY J TR OOOO 00
    # Pad seq to 7 digits
    seq = seq_str.zfill(7)
    year = year_str.zfill(4)
    j = j_str
    tr = tr_str.zfill(2)
    oooo = oooo_str.zfill(4)
    
    number_str = f"{seq}{year}{j}{tr}{oooo}00"
    num = int(number_str)
    mod = num % 97
    check = 98 - mod
    return f"{check:02d}"

print("Check digit for 1261994, 2026, 8, 13, 0000:")
print(calculate_cnj_check_digit("1261994", "2026", "8", "13", "0000"))

print("Check digit for 1261994, 2026, 8, 13, 0024:")
print(calculate_cnj_check_digit("1261994", "2026", "8", "13", "0024"))

print("Check digit for 12619945 (as sequence?):")
try:
    print(calculate_cnj_check_digit("12619945", "2026", "8", "13", "0000"))
except Exception as e:
    print(e)
