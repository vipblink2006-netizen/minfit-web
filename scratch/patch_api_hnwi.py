import sys
with open("workflow_api.py", "r") as f:
    content = f.read()

target1 = """    cash_remaining_after_move_in = available_cash - total_upfront_needed"""
replacement1 = """    cash_remaining_after_move_in = available_cash - total_upfront_needed

    hnwi_strategy = None
    if available_cash >= project_price * Decimal("1.05"):
        outright_cash_left = available_cash - (project_price + initial_move_in_capex)
        leverage_cash_left = cash_remaining_after_move_in
        hnwi_strategy = {
            "has_dual_option": True,
            "outright_cash_left": float(outright_cash_left),
            "leverage_cash_left": float(leverage_cash_left),
        }
        # Cập nhật lời khuyên cho action plan HNWI
        action_plan = []
        action_plan.append(f"Kịch bản 1 (Mua đứt): Thanh toán 100%, giữ lại {outright_cash_left/1e9:.1f} tỷ tiền mặt. Lợi ích: Nhận chiết khấu tối đa, an toàn tuyệt đối, DTI = 0%.")
        action_plan.append(f"Kịch bản 2 (Đòn bẩy): Dùng gói HTLS, giữ lại {leverage_cash_left/1e9:.1f} tỷ tiền mặt. Lợi ích: Mang {leverage_cash_left/1e9:.1f} tỷ đi đầu tư sinh lời ở kênh khác (chứng khoán, trái phiếu, kinh doanh) để bù đắp lãi suất thả nổi sau ưu đãi.")"""

target2 = """    shock_level = "safe" if payment_shock_ratio <= Decimal("1.4") else "caution" if payment_shock_ratio <= Decimal("1.8") else "danger"

    shock_suggestion = ""
"""
replacement2 = """    shock_level = "safe" if payment_shock_ratio <= Decimal("1.4") else "caution" if payment_shock_ratio <= Decimal("1.8") else "danger"

    if hnwi_strategy:
        shock_level = "safe"
        payment_shock_ratio = Decimal("1.0")

    shock_suggestion = ""
"""

target3 = """    action_plan = []
    if assessment.rank_class == "A":
"""
replacement3 = """    if not hnwi_strategy:
        action_plan = []
    if assessment.rank_class == "A" and not hnwi_strategy:
"""

target4 = """        "filter_summary": {"""
replacement4 = """        "hnwi_strategy": hnwi_strategy,
        "filter_summary": {"""

if target1 in content and target2 in content and target3 in content and target4 in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    content = content.replace(target3, replacement3)
    content = content.replace(target4, replacement4)
    with open("workflow_api.py", "w") as f:
        f.write(content)
    print("PATCH WORKFLOW SUCCESSFUL")
else:
    print("TARGET NOT FOUND:")
    print("T1", target1 in content)
    print("T2", target2 in content)
    print("T3", target3 in content)
    print("T4", target4 in content)
