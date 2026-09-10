import re

with open('database.py', 'r') as f:
    content = f.read()

# Fix Amenities
content = content.replace(
    'INSERT INTO Amenities(code,label) ON CONFLICT(code) DO UPDATE SET label=EXCLUDED.label VALUES (?,?)',
    'INSERT INTO Amenities(code,label) VALUES (?,?) ON CONFLICT(code) DO UPDATE SET label=EXCLUDED.label'
)

# Fix PersonaWeights
content = content.replace(
    'INSERT INTO PersonaWeights(persona_code,price_weight,distance_weight,amenity_weight) ON CONFLICT(persona_code) DO UPDATE SET price_weight=EXCLUDED.price_weight, distance_weight=EXCLUDED.distance_weight, amenity_weight=EXCLUDED.amenity_weight VALUES (?,?,?,?)',
    'INSERT INTO PersonaWeights(persona_code,price_weight,distance_weight,amenity_weight) VALUES (?,?,?,?) ON CONFLICT(persona_code) DO UPDATE SET price_weight=EXCLUDED.price_weight, distance_weight=EXCLUDED.distance_weight, amenity_weight=EXCLUDED.amenity_weight'
)

# Fix Users
content = content.replace(
    'INSERT INTO Users (id, name, email, phone, password_hash, role, agency, status, clients_count, projects_count, units_sold, created_at, last_active) ON CONFLICT(id) DO UPDATE SET',
    'INSERT INTO Users (id, name, email, phone, password_hash, role, agency, status, clients_count, projects_count, units_sold, created_at, last_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, CURRENT_TIMESTAMP, \'Vừa xong\') ON CONFLICT(id) DO UPDATE SET'
)
content = content.replace(
    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, CURRENT_TIMESTAMP, \'Vừa xong\')\n            ON CONFLICT(id) DO UPDATE SET',
    'ON CONFLICT(id) DO UPDATE SET'
)

with open('database.py', 'w') as f:
    f.write(content)
