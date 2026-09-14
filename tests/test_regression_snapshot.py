from __future__ import annotations

import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import sys

# Add parent directory to sys.path to import workflow_api
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow_api import analyze

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)
 
DECIMAL_TOLERANCE = Decimal("0.01")
 
SAMPLE_PROFILES: dict[str, dict[str, Any]] = {
    "family_standard_safe": {
        "persona": "family_with_children",
        "property_type": "chung_cu",
        "monthly_income": "45000000",
        "existing_debt": "0",
        "available_cash": "2000000000",
        "age": "35",
        "child_count": 1,
        "term_years": 20,
        "loan_ratio_percent": "60",
        "transport_mode": "motorbike",
        "has_car": False,
        "selected_project_ids": [],
    },
    "low_income_floor_trigger": {
        "persona": "single",
        "property_type": "chung_cu",
        "monthly_income": "8000000",
        "existing_debt": "0",
        "available_cash": "300000000",
        "age": "26",
        "child_count": 0,
        "term_years": 20,
        "loan_ratio_percent": "70",
        "transport_mode": "motorbike",
        "has_car": False,
        "selected_project_ids": [],
    },
    "empty_string_numeric_fields": {
        "persona": "young_couple",
        "property_type": "chung_cu",
        "monthly_income": "35000000",
        "existing_debt": "0",
        "available_cash": "800000000",
        "age": "",
        "child_count": "",
        "term_years": "",
        "loan_ratio_percent": "70",
        "transport_mode": "car",
        "has_car": True,
        "selected_project_ids": [],
    },
    "tho_cu_transfer_tax": {
        "persona": "family_with_children",
        "property_type": "tho_cu",
        "monthly_income": "60000000",
        "existing_debt": "0",
        "available_cash": "1500000000",
        "age": "40",
        "child_count": 2,
        "term_years": 20,
        "loan_ratio_percent": "50",
        "transport_mode": "car",
        "has_car": True,
        "has_garage": False,
        "selected_project_ids": [],
    },
    "retired_age_boundary": {
        "persona": "retired",
        "property_type": "chung_cu",
        "monthly_income": "40000000",
        "existing_debt": "0",
        "available_cash": "3000000000",
        "age": "58",
        "child_count": 0,
        "term_years": 15,
        "loan_ratio_percent": "40",
        "transport_mode": "motorbike",
        "has_car": False,
        "selected_project_ids": [],
    },
    "hnwi_outright_purchase": {
        "persona": "family_with_children",
        "property_type": "thap_tang",
        "monthly_income": "150000000",
        "existing_debt": "0",
        "available_cash": "15000000000",
        "age": "45",
        "child_count": 2,
        "term_years": 20,
        "loan_ratio_percent": "0",
        "transport_mode": "car",
        "has_car": True,
        "selected_project_ids": [],
    },
    "existing_debt_heavy": {
        "persona": "young_couple",
        "property_type": "chung_cu",
        "monthly_income": "50000000",
        "existing_debt": "15000000",
        "available_cash": "900000000",
        "age": "30",
        "child_count": 0,
        "term_years": 20,
        "loan_ratio_percent": "70",
        "transport_mode": "car",
        "has_car": True,
        "selected_project_ids": [],
    },
    "clearly_negative_cashflow": {
        "persona": "family_with_children",
        "property_type": "chung_cu",
        "monthly_income": "25000000",
        "existing_debt": "5000000",
        "available_cash": "200000000",
        "age": "33",
        "child_count": 2,
        "term_years": 20,
        "loan_ratio_percent": "85",
        "transport_mode": "car",
        "has_car": True,
        "selected_project_ids": [],
    },
}

def _extract_tracked_values(analyze_result: dict) -> dict[str, Any]:
    first_project_result = analyze_result.get("results", [analyze_result])[0]
 
    extracted: dict[str, Any] = {}
    
    # Map correct paths in JSON
    fb = first_project_result.get("financial_breakdown", {})
    extracted["thb_ratio"] = str(fb.get("thb_ratio"))
    extracted["real_fcf"] = str(fb.get("real_fcf"))
    extracted["fcf_status"] = str(fb.get("fcf_status"))
    extracted["cash_remaining_after_move_in"] = str(fb.get("cash_remaining_after_move_in"))
    extracted["survival_runway_months"] = str(fb.get("survival_runway_months"))
    
    extracted["verdict_status"] = str(first_project_result.get("verdict", {}).get("status"))
    extracted["rank_class"] = str(first_project_result.get("rank_class"))
    extracted["hard_filter_status"] = str(first_project_result.get("hard_filter_status"))
    
    extracted["payment_shock_ratio"] = str(first_project_result.get("payment_shock", {}).get("ratio"))
    extracted["is_default_risk"] = str(first_project_result.get("stress_test", {}).get("risk"))

    return extracted
 
def _values_differ(old: Any, new: Any) -> bool:
    if old is None or new is None:
        return old != new
    try:
        old_dec = Decimal(str(old))
        new_dec = Decimal(str(new))
        return abs(old_dec - new_dec) > DECIMAL_TOLERANCE
    except Exception:
        return old != new
 
def _load_snapshot(name: str) -> dict | None:
    path = SNAPSHOT_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
 
def _save_snapshot(name: str, data: dict) -> None:
    path = SNAPSHOT_DIR / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
 
@pytest.mark.parametrize("profile_name", list(SAMPLE_PROFILES.keys()))
def test_analyze_matches_snapshot(profile_name: str, request):
    payload = SAMPLE_PROFILES[profile_name]
    result = analyze(payload)
    current_snapshot = _extract_tracked_values(result)
    saved_snapshot = _load_snapshot(profile_name)
 
    update_mode = request.config.getoption("--snapshot-update", default=False)
 
    if saved_snapshot is None or update_mode:
        _save_snapshot(profile_name, current_snapshot)
        if saved_snapshot is None:
            pytest.skip(f"[{profile_name}] Chưa có snapshot — đã tạo mới. Hãy chạy lại lần nữa để test thực sự so sánh.")
        else:
            pytest.skip(f"[{profile_name}] Đã cập nhật snapshot theo yêu cầu --snapshot-update.")
        return
 
    diffs = []
    TRACKED_FIELDS = list(current_snapshot.keys())
    for field in TRACKED_FIELDS:
        old_val = saved_snapshot.get(field)
        new_val = current_snapshot.get(field)
        if _values_differ(old_val, new_val):
            diffs.append(f"  - {field}: {old_val!r}  ->  {new_val!r}")
 
    if diffs:
        diff_report = "\n".join(diffs)
        pytest.fail(
            f"\n[{profile_name}] Kết quả analyze() đã LỆCH so với snapshot đã lưu:\n"
            f"{diff_report}\n\n"
            f"Nếu đây là thay đổi CHỦ ĐÍCH (bạn cố tình sửa business rule):\n"
            f"  pytest {__file__} -v --snapshot-update -k {profile_name}\n"
        )
 
def pytest_addoption(parser):
    parser.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        help="Ghi đè snapshot hiện tại.",
    )
 
def test_no_crash_on_empty_string_inputs():
    payload = dict(SAMPLE_PROFILES["empty_string_numeric_fields"])
    try:
        result = analyze(payload)
    except (ValueError, TypeError) as exc:
        pytest.fail(f"analyze() vẫn crash với input rỗng chuỗi — safe_int() chưa bao phủ hết mọi điểm parse. Lỗi: {exc}")
    assert result is not None
 
def test_low_income_floor_shows_warning():
    payload = SAMPLE_PROFILES["low_income_floor_trigger"]
    result = analyze(payload)
    first_result = result.get("results", [result])[0]
 
    # Warning was added to customer_advice!
    customer_advice = first_result.get("verdict", {}).get("customer_advice", [])
    warning_text = " ".join(str(x) for x in customer_advice)
 
    assert "10" in warning_text and ("giả định" in warning_text.lower() or "cảnh báo" in warning_text.lower()), "Không tìm thấy cảnh báo về sàn thu nhập 10 triệu trong customer_advice."
 
def test_retired_client_age_boundary_rejected_or_warned():
    payload = SAMPLE_PROFILES["retired_age_boundary"]
    result = analyze(payload)
    first_result = result.get("results", [result])[0]
 
    hard_filter_status = first_result.get("hard_filter_status")
    assert hard_filter_status in ("WARNING", "REJECT")
 
def test_hnwi_strategy_overrides_rank_to_a():
    payload = SAMPLE_PROFILES["hnwi_outright_purchase"]
    result = analyze(payload)
    first_result = result.get("results", [result])[0]
 
    assert first_result.get("verdict", {}).get("status") == "RECOMMENDED_BUY"
    assert first_result.get("rank_class") == "A"
