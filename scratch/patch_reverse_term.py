import sys
with open("workflow_api.py", "r") as f:
    content = f.read()

target = """    if payment_shock_ratio > Decimal("1.8"):
        term_years = int(payload.get("term_years", 20))
        suggested_term = 30 if term_years < 30 else 35
        suggested_pmt = round((pmt_after * Decimal(term_years) / Decimal(suggested_term)) / Decimal("1000000"), 1)
        shock_suggestion = f"Cú sốc thả nổi tháng {shock_month} tăng vọt {payment_shock_ratio:.1f} lần (từ {pmt_before/Decimal('1000000'):.1f} tr lên {pmt_after/Decimal('1000000'):.1f} tr). Đề xuất: Kéo dài thời hạn vay từ {term_years} năm lên {suggested_term} năm để hạ PMT xuống ~{suggested_pmt} triệu/tháng." """

replacement = """    if payment_shock_ratio > Decimal("1.8") or thb_ratio > Decimal("50"):
        term_years = int(payload.get("term_years", 20))
        # REVERSE ENGINEERING THE LOAN TERM
        # Target: total_housing_cost / net_acceptable_income <= 0.5
        # => Target pmt_floating <= net_acceptable_income * 0.5 - total_housing_fees
        target_max_pmt = (net_acceptable_income * Decimal("0.5")) - total_housing_fees
        if target_max_pmt > Decimal("0") and pmt_after > target_max_pmt:
            # Approximate linear scaling for annuity term
            required_scale = float(pmt_after / target_max_pmt)
            calc_term = int(term_years * required_scale)
            # Find closest standard banking term (10, 15, 20, 25, 30, 35)
            standard_terms = [10, 15, 20, 25, 30, 35]
            suggested_term = next((t for t in standard_terms if t >= calc_term), 35)
            if suggested_term <= term_years:
                suggested_term = 35 if term_years < 35 else term_years
                
            suggested_pmt = round((pmt_after * Decimal(term_years) / Decimal(suggested_term)) / Decimal("1000000"), 1)
            shock_suggestion = f"Dòng tiền thâm hụt (PMT {pmt_after/Decimal('1000000'):.1f} tr). Tư vấn may đo: Kéo dài thời hạn vay từ {term_years} năm lên {suggested_term} năm để hạ mức trả góp xuống ~{suggested_pmt} tr/tháng, đảm bảo Thặng dư an toàn."
        elif payment_shock_ratio > Decimal("1.8"):
            suggested_term = 30 if term_years < 30 else 35
            suggested_pmt = round((pmt_after * Decimal(term_years) / Decimal(suggested_term)) / Decimal("1000000"), 1)
            shock_suggestion = f"Cú sốc thả nổi tháng {shock_month} tăng vọt {payment_shock_ratio:.1f} lần. Đề xuất: Kéo dài thời hạn vay lên {suggested_term} năm để hạ PMT xuống ~{suggested_pmt} triệu/tháng." """

if target in content:
    content = content.replace(target, replacement)
    with open("workflow_api.py", "w") as f:
        f.write(content)
    print("PATCH REVERSE TERM SUCCESSFUL")
else:
    print("TARGET NOT FOUND")
