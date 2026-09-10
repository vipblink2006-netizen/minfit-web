with open('index.html', 'r') as f:
    content = f.read()

old_text = "Chỉ cần copy nguyên văn tin nhắn từ Zalo/Telegram/Email của CĐT có chứa các link <b>Google Drive</b>, <b>Bảng hàng Sheets</b>, <b>Kuula 360</b> dán vào khung dưới."
new_text = "Chỉ cần copy nguyên văn tin nhắn từ Zalo/Telegram/Email của CĐT có chứa các link <b>Google Drive</b>, <b>Bảng hàng Sheets</b>, <b>Slide Đào tạo</b>, hoặc <b>Kuula 360</b> dán vào khung dưới."

content = content.replace(old_text, new_text)

with open('index.html', 'w') as f:
    f.write(content)
