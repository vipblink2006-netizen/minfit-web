with open('database.py', 'r') as f:
    content = f.read()

# Fix usr_admin and brk_moigioi
content = content.replace("'Vừa xong'", "CURRENT_TIMESTAMP")

with open('database.py', 'w') as f:
    f.write(content)
