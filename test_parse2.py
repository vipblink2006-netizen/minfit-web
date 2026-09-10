from workflow_api import parse_raw_project_text
import json

text = """Bán gấp căn 3PN Duplex Masteri Waterfront
Giá siêu rẻ chỉ 5 tỏi 2 hoặc 7x tr/m
Bàn giao 2024, ở ngay!
Chiết khấu 10%, HTLS 18 tháng
Tiện ích: bể bơi, trường học
[https://docs.google.com/spreadsheets/d/abc]"""

res = parse_raw_project_text(text)
print(json.dumps(res, indent=2, ensure_ascii=False))
