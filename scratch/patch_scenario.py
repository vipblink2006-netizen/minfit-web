import sys
with open("workflow_api.py", "r") as f:
    content = f.read()

target = """        # SMART RECOMMENDATION ENGINE (AUTO)
        if base_scheme == "auto":
            if avail_cash >= project.price_min_vnd * Decimal("1.05"):
                scheme_to_use = "early_payment"
                loc_payload["payment_scheme"] = scheme_to_use # Patch for downstream logic
            else:
                scheme_to_use = "loan_htls" if market_segment == "primary" else "bank_vcb"
                loc_payload["payment_scheme"] = scheme_to_use
        else:
            scheme_to_use = base_scheme"""

replacement = """        # SMART RECOMMENDATION ENGINE (AUTO)
        if base_scheme == "auto":
            # For HNWI with excess cash, we simulate HTLS to show leverage, but we show Dual Options in the UI.
            scheme_to_use = "loan_htls" if market_segment == "primary" else "bank_vcb"
            loc_payload["payment_scheme"] = scheme_to_use
        else:
            scheme_to_use = base_scheme"""

if target in content:
    content = content.replace(target, replacement)
    with open("workflow_api.py", "w") as f:
        f.write(content)
    print("PATCH SCENARIO SUCCESSFUL")
else:
    print("TARGET NOT FOUND")
