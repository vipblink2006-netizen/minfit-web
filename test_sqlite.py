import sqlite3
import traceback
conn = sqlite3.connect("minfit_data.db")
try:
    conn.execute('''
    INSERT INTO Projects(
        id, name, area, developer, price_min_vnd, price_avg_mil_m2, price_min_mil_m2, price_max_mil_m2,
        area_m2, area_min_m2, area_max_m2, layout_types, lat, lng, management_fee_per_m2, bedrooms,
        raw_amenities, handover_status, handover_year, is_handed_over, payment_policy, grace_period_months,
        inventory_link, risk_note, is_global, created_by_role, broker_id, approval_status, crawl_url,
        crawl_frequency, links_json, units_json, raw_source_text, is_active
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name, area=excluded.area, developer=excluded.developer, price_min_vnd=excluded.price_min_vnd,
        price_avg_mil_m2=excluded.price_avg_mil_m2, price_min_mil_m2=excluded.price_min_mil_m2, price_max_mil_m2=excluded.price_max_mil_m2,
        area_m2=excluded.area_m2, area_min_m2=excluded.area_min_m2, area_max_m2=excluded.area_max_m2, layout_types=excluded.layout_types,
        lat=excluded.lat, lng=excluded.lng, management_fee_per_m2=excluded.management_fee_per_m2, bedrooms=excluded.bedrooms,
        raw_amenities=excluded.raw_amenities, handover_status=excluded.handover_status, handover_year=excluded.handover_year,
        is_handed_over=excluded.is_handed_over, payment_policy=excluded.payment_policy, grace_period_months=excluded.grace_period_months,
        inventory_link=excluded.inventory_link, risk_note=excluded.risk_note, is_global=excluded.is_global,
        approval_status=excluded.approval_status, crawl_url=excluded.crawl_url, crawl_frequency=excluded.crawl_frequency,
        links_json=excluded.links_json, units_json=excluded.units_json, raw_source_text=excluded.raw_source_text,
        is_active=excluded.is_active, updated_at=CURRENT_TIMESTAMP
    ''',
    ("pid123", "Test", "Area", "", 1, 1, 1, 1, 1, 1, 1, "", 1.0, 1.0, 1, "", "", "", 2026, 0, "", 0, "", "", 0, "broker", "broker", "approved", "", "daily", "{}", "[]", "", 1))
    conn.commit()
    print("Executed successfully!")
except Exception as e:
    traceback.print_exc()
