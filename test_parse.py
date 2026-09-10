from workflow_api import parse_raw_project_text
import json

text = """Bảng hàng Imperia Sky Park
[https://docs.google.com/spreadsheets/d/1FR-qtrHfuSu3jJfOvEE-fxpXfYAR3iMF4p6vgOfyHH8/edit?gid=0#gid=0]
📖 Tài liệu dự án:
✅ Tổng hợp thông tin: [https://drive.google.com/drive/folders/1YE91uX3yISmaruQVmVMsa-ZTSAcnlH6l]
✅ Mặt bằng dự án: [https://drive.google.com/drive/folders/1gYXso2YUoGHcOPQQt-DSVA-pLF9I9Ece]
✅ Hình ảnh dự án: [https://drive.google.com/drive/folders/1IxWcdCEJ4xzcSaoMTFPk0FFVqkSqjhpQ]"""

res = parse_raw_project_text(text)
print(json.dumps(res, indent=2, ensure_ascii=False))
