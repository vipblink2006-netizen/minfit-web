with open('database.py', 'r') as f:
    content = f.read()

# Fix load_broker_selection_from_db
content = content.replace(
    'return [r["project_id"] for r in rows]',
    'return [to_dict(r)["project_id"] for r in rows]'
)

# Fix toggle_user_status
content = content.replace(
    'new_status = "locked" if row["status"] == "active" else "active"',
    'new_status = "locked" if to_dict(row)["status"] == "active" else "active"'
)

# Fix load_persona_weights_from_database
content = content.replace(
    'weights[row["persona_code"]] = {\n                "price": Decimal(str(row["price_weight"])),\n                "distance": Decimal(str(row["distance_weight"])),\n                "amenities": Decimal(str(row["amenity_weight"])),\n            }',
    'd = to_dict(row)\n            weights[d["persona_code"]] = {\n                "price": Decimal(str(d["price_weight"])),\n                "distance": Decimal(str(d["distance_weight"])),\n                "amenities": Decimal(str(d["amenity_weight"])),\n            }'
)

with open('database.py', 'w') as f:
    f.write(content)
