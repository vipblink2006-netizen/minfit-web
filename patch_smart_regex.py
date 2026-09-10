import re

with open('workflow_api.py', 'r') as f:
    content = f.read()

# I will replace the # Detect Price & Area section and below
old_section = """    # Detect Price & Area
    price_mil_m2 = 0.0
    total_price_billion = 0.0

    bil_price_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)\\s*(?:-|đến|–)?\\s*(\\d+(?:[\\.,]\\d+)?)?\\s*(?:tỷ|ty|tỷ\\s*đồng|bil)', text, re.IGNORECASE)
    if bil_price_match:
        val1 = float(bil_price_match.group(1).replace(",", "."))
        val2 = float(bil_price_match.group(2).replace(",", ".")) if bil_price_match.group(2) else val1
        total_price_billion = round((val1 + val2) / 2.0, 2)

    m2_price_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)\\s*(?:-|đến|–)?\\s*(\\d+(?:[\\.,]\\d+)?)?\\s*(?:tr(?:iệu)?(?:/m[2²])?|triệu/m[2²]|tr/m[2²])', text, re.IGNORECASE)
    if m2_price_match:
        val1 = float(m2_price_match.group(1).replace(",", "."))
        val2 = float(m2_price_match.group(2).replace(",", ".")) if m2_price_match.group(2) else val1
        cand_m2 = round((val1 + val2) / 2.0, 1)
        if cand_m2 >= 15:
            price_mil_m2 = cand_m2

    area_m2 = 70.0
    area_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)\\s*(?:-|đến|–)?\\s*(\\d+(?:[\\.,]\\d+)?)?\\s*(?:m[2²]|mét\\s*vuông)', text, re.IGNORECASE)
    if area_match:
        val1 = float(area_match.group(1).replace(",", "."))
        val2 = float(area_match.group(2).replace(",", ".")) if area_match.group(2) else val1
        if 20 <= val1 <= 500:
            area_m2 = round((val1 + val2) / 2.0, 1)

    if total_price_billion > 0:
        price_min_vnd = int(total_price_billion * 1_000_000_000)
        if price_mil_m2 == 0:
            price_mil_m2 = round(float(price_min_vnd) / area_m2 / 1_000_000, 1)
    elif price_mil_m2 > 0:
        price_min_vnd = int(price_mil_m2 * area_m2 * 1_000_000)
        total_price_billion = round(float(price_min_vnd) / 1_000_000_000, 2)
    else:
        price_mil_m2 = 75.0
        price_min_vnd = int(price_mil_m2 * area_m2 * 1_000_000)
        total_price_billion = round(float(price_min_vnd) / 1_000_000_000, 2)

    # Detect Amenities"""

new_section = """    # Detect Price & Area (Smart Regex 2.0)
    price_mil_m2 = 0.0
    total_price_billion = 0.0

    # Support 'tỏi', 'x', etc.
    bil_price_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)?\\s*(?:tỷ|ty|tỏi|tỷ\\s*đồng|bil)\\s*([x\\d]+)?', text, re.IGNORECASE)
    if bil_price_match:
        val1_str = bil_price_match.group(1)
        suffix = bil_price_match.group(2)
        if val1_str:
            base = float(val1_str.replace(",", "."))
            if suffix and 'x' in suffix.lower():
                base += 0.5  # '3 tỷ x' -> 3.5
            elif suffix and suffix.isdigit():
                base += float(suffix) / 10.0  # '3 tỷ 2' -> 3.2
            total_price_billion = base

    # Support 'tr/m', 'tr/m2', 'triệu', 'x tr/m'
    m2_price_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)([xX])?\\s*(?:-|đến|–)?\\s*(\\d+(?:[\\.,]\\d+)?)?([xX])?\\s*(?:tr(?:iệu)?(?:/m[2²]?)?|tr/m)', text, re.IGNORECASE)
    if m2_price_match:
        val1_str = m2_price_match.group(1)
        has_x1 = m2_price_match.group(2)
        val2_str = m2_price_match.group(3)
        has_x2 = m2_price_match.group(4)
        
        val1 = float(val1_str.replace(",", ".")) if val1_str else 0
        if has_x1: val1 += 5
        
        if val2_str:
            val2 = float(val2_str.replace(",", "."))
            if has_x2: val2 += 5
        else:
            val2 = val1
            
        cand_m2 = round((val1 + val2) / 2.0, 1)
        if cand_m2 >= 15:
            price_mil_m2 = cand_m2

    area_m2 = 70.0
    area_match = re.search(r'(\\d+(?:[\\.,]\\d+)?)\\s*(?:-|đến|–)?\\s*(\\d+(?:[\\.,]\\d+)?)?\\s*(?:m[2²]|mét\\s*vuông)', text, re.IGNORECASE)
    if area_match:
        val1 = float(area_match.group(1).replace(",", "."))
        val2 = float(area_match.group(2).replace(",", ".")) if area_match.group(2) else val1
        if 20 <= val1 <= 500:
            area_m2 = round((val1 + val2) / 2.0, 1)

    if total_price_billion > 0:
        price_min_vnd = int(total_price_billion * 1_000_000_000)
        if price_mil_m2 == 0:
            price_mil_m2 = round(float(price_min_vnd) / area_m2 / 1_000_000, 1)
    elif price_mil_m2 > 0:
        price_min_vnd = int(price_mil_m2 * area_m2 * 1_000_000)
        total_price_billion = round(float(price_min_vnd) / 1_000_000_000, 2)
    else:
        price_mil_m2 = 75.0
        price_min_vnd = int(price_mil_m2 * area_m2 * 1_000_000)
        total_price_billion = round(float(price_min_vnd) / 1_000_000_000, 2)

    # Detect Layout Types & Bedrooms
    found_bds = re.findall(r'(studio|duplex|penthouse|\\d\\s*pn(?:\\+\\d)?)', text, re.IGNORECASE)
    layout_types = "Studio - 3PN"
    bedrooms = "2PN"
    if found_bds:
        bds_clean = []
        for b in found_bds:
            bl = b.lower().replace(" ", "")
            if bl == "studio": bds_clean.append("Studio")
            elif bl == "duplex": bds_clean.append("Duplex")
            elif bl == "penthouse": bds_clean.append("Penthouse")
            else: bds_clean.append(bl.upper())
        bds_clean = list(dict.fromkeys(bds_clean))
        layout_types = " - ".join(bds_clean)
        bedrooms = bds_clean[0] if bds_clean else "2PN"

    # Detect Payment Policy & Grace Period
    payment_policy = ""
    grace_period_months = 0
    htls_match = re.search(r'(?:htls|hỗ trợ lãi suất|vay).*?(\\d{1,2})\\s*(?:tháng|m)', text, re.IGNORECASE)
    if htls_match:
        grace_period_months = int(htls_match.group(1))
        payment_policy += f"HTLS {grace_period_months} tháng. "
    
    ck_match = re.search(r'(?:chiết khấu|ck).*?(\\d{1,2}(?:[\\.,]\\d+)?)\\s*%', text, re.IGNORECASE)
    if ck_match:
        payment_policy += f"Chiết khấu {ck_match.group(1)}%. "
        
    if not payment_policy:
        payment_policy = "Thanh toán theo tiến độ chuẩn"

    # Detect Handover
    handover_year = 2026
    handover_status = "Đang mở bán"
    is_handed_over = False
    
    ho_match = re.search(r'(?:bàn giao|nhận nhà).*?(202\\d)', text, re.IGNORECASE)
    if ho_match:
        handover_year = int(ho_match.group(1))
        if handover_year <= 2024:
            handover_status = "Đã bàn giao"
            is_handed_over = True
            
    if any(k in text.lower() for k in ["sẵn sàng ở", "ở ngay", "nhận nhà ngay", "đã bàn giao"]):
        handover_status = "Đã bàn giao"
        is_handed_over = True

    # Detect Amenities"""

content = content.replace(old_section, new_section)

# Also update the hardcoded return dict
return_old = """            "layout_types": "Studio - 3PN",
            "lat": detected_lat,
            "lng": detected_lng,
            "management_fee_per_m2": 15000.0,
            "bedrooms": "2PN",
            "amenities": amenity_codes,
            "raw_amenities": ", ".join(AMENITY_LABELS.get(a, a) for a in amenity_codes),
            "handover_status": "Đang mở bán",
            "handover_year": 2026,
            "is_handed_over": False,
            "payment_policy": "Chiết khấu mở bán & Hỗ trợ vay ngân hàng 70%",
            "grace_period_months": 24,"""

return_new = """            "layout_types": layout_types,
            "lat": detected_lat,
            "lng": detected_lng,
            "management_fee_per_m2": 15000.0,
            "bedrooms": bedrooms,
            "amenities": amenity_codes,
            "raw_amenities": ", ".join(AMENITY_LABELS.get(a, a) for a in amenity_codes),
            "handover_status": handover_status,
            "handover_year": handover_year,
            "is_handed_over": is_handed_over,
            "payment_policy": payment_policy.strip(),
            "grace_period_months": grace_period_months if grace_period_months > 0 else 0,"""

content = content.replace(return_old, return_new)

with open('workflow_api.py', 'w') as f:
    f.write(content)
