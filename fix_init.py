with open('database.py', 'r') as f:
    content = f.read()

# Add ensure_database call right before __main__ block
content = content.replace(
    'if __name__ == "__main__":',
    '# Tự động tạo bảng nếu chưa có\ntry:\n    ensure_database()\nexcept Exception as e:\n    print("Lỗi khởi tạo DB:", e)\n\nif __name__ == "__main__":'
)

with open('database.py', 'w') as f:
    f.write(content)
