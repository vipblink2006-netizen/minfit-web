with open('database.py', 'r') as f:
    content = f.read()

seeding_code = """
        # Seed logic for Postgres
        raw_projects = json.loads(PROJECTS_JSON.read_text(encoding="utf-8"))
        
        # Check if already seeded
        row = connection.execute("SELECT COUNT(*) as count FROM Projects").fetchone()
        if to_dict(row)["count"] == 0:
            for code, label in AMENITY_LABELS.items():
                connection.execute("INSERT INTO Amenities(code,label) VALUES (?,?) ON CONFLICT(code) DO UPDATE SET label=EXCLUDED.label", (code, label))

            for item in raw_projects:
                connection.execute(
                    '''
                    INSERT INTO Projects (
                        id, name, area, developer, price_min_vnd, price_avg_mil_m2, price_min_mil_m2, price_max_mil_m2,
                        area_m2, area_min_m2, area_max_m2, layout_types, lat, lng, management_fee_per_m2, bedrooms,
                        raw_amenities, handover_status, handover_year, is_handed_over, payment_policy, grace_period_months,
                        inventory_link, risk_note, is_global, created_by_role, approval_status, crawl_url, crawl_frequency,
                        links_json, units_json, is_active
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)
                    ON CONFLICT(id) DO NOTHING
                    ''',
                    (
                        item["id"], item["name"], item["area"], item.get("developer", ""),
                        item["price_min_vnd"], item.get("price_avg_mil_m2", 0), item.get("price_min_mil_m2", 0), item.get("price_max_mil_m2", 0),
                        item["area_m2"], item.get("area_min_m2", 0), item.get("area_max_m2", 0), item.get("layout_types", ""),
                        item["lat"], item["lng"], item["management_fee_per_m2"], item["bedrooms"],
                        item.get("raw_amenities", ""), item.get("handover_status", ""), item.get("handover_year", 0), 1 if item.get("is_handed_over") else 0,
                        item.get("payment_policy", ""), item.get("grace_period_months", 0), item.get("inventory_link", ""), item.get("risk_note", ""),
                        item.get("is_global", 1), item.get("created_by_role", "admin"), item.get("approval_status", "approved"),
                        item.get("crawl_url", ""), item.get("crawl_frequency", "daily"), json.dumps(item.get("links", {})), json.dumps(item.get("units", []))
                    ),
                )
                for a in item["amenities"]:
                    connection.execute("INSERT INTO ProjectAmenities(project_id, amenity_code) VALUES (?,?) ON CONFLICT(project_id, amenity_code) DO NOTHING", (item["id"], a))

            for code, weights in PERSONA_WEIGHTS.items():
                connection.execute(
                    "INSERT INTO PersonaWeights VALUES (?,?,?,?) ON CONFLICT(persona_code) DO UPDATE SET price_weight=EXCLUDED.price_weight, distance_weight=EXCLUDED.distance_weight, amenity_weight=EXCLUDED.amenity_weight",
                    (code, float(weights["price"]), float(weights["distance"]), float(weights["amenities"])),
                )
            connection.commit()
"""

# Insert seeding code before returning from _ensure_postgres_database
content = content.replace(
    '        );\n        \'\'\')\n    return DatabaseStatus("postgres", "minfit", 0, 0)',
    '        );\n        \'\'\')\n' + seeding_code + '    return DatabaseStatus("postgres", "minfit", 0, 0)'
)

with open('database.py', 'w') as f:
    f.write(content)
