with open('database.py', 'r') as f:
    content = f.read()

content = content.replace(
    'inventory_link=excluded.inventory_link, risk_note=excluded.risk_note, is_global=excluded.is_global,\n                approval_status=excluded.approval_status,',
    'inventory_link=excluded.inventory_link, risk_note=excluded.risk_note, is_global=excluded.is_global, broker_id=excluded.broker_id,\n                approval_status=excluded.approval_status,'
)

with open('database.py', 'w') as f:
    f.write(content)
