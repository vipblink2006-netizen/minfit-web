import re
line = "Bảng hàng Imperia Sky Park"
clean_first = re.sub(r'^[\s\W\d\.\-\*•–🔥🌟👉✨💥]+', '', line).strip()
print("clean_first:", repr(clean_first))
