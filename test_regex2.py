import re
text = """Bảng hàng Imperia Sky Park
[https://docs.google.com/spreadsheets/d/1FR-qtrHfuSu3jJfOvEE-fxpXfYAR3iMF4p6vgOfyHH8/edit?gid=0#gid=0]
📖 Tài liệu dự án:
✅ Tổng hợp thông tin: [https://drive.google.com/drive/folders/1YE91uX3yISmaruQVmVMsa-ZTSAcnlH6l]
✅ Mặt bằng dự án: [https://drive.google.com/drive/folders/1gYXso2YUoGHcOPQQt-DSVA-pLF9I9Ece]
✅ Hình ảnh dự án: [https://drive.google.com/drive/folders/1IxWcdCEJ4xzcSaoMTFPk0FFVqkSqjhpQ]"""

name_match = re.search(r'(?:dự án|project|khu căn hộ|tổ hợp)[ \t]*[:\-–]?[ \t]*([^\n\r,;🔥🌟👉✨💥]+)', text, re.IGNORECASE)
if name_match:
    print("MATCH:", repr(name_match.group(1)))
else:
    print("NO MATCH")
