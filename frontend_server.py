from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json

import datetime
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)
from pathlib import Path
import os
import socket
from urllib.parse import parse_qs, urlparse
from workflow_api import (
    analyze,
    authenticate_user,
    create_client,
    list_clients,
    delete_client,
    create_or_update_project,
    delete_project,
    get_broker_selection,
    get_system_stats,
    list_projects,
    list_users,
    parse_raw_project_text,
    save_broker_selection,
    save_user,
    sync_market_data,
    toggle_project_status,
    toggle_user_status,
    verify_session,
    revoke_session,
)
from loan_dti import (
    FinancialProfile,
    LoanScenario,
    simulate_loan,
    annuity_payment,
    calculate_dti_score,
    calculate_ltv_score,
    decimal_value,
)
from decimal import Decimal


ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("HOST", "0.0.0.0")
DEFAULT_PORT = int(os.environ.get("PORT", "5173"))


class ReactRouterHandler(SimpleHTTPRequestHandler):
    """Serve static assets and fall back to index.html for React Router routes with stateful session auth middleware."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _set_cors_headers(self) -> None:
        origin = self.headers.get("Origin", "")
        allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost", "http://127.0.0.1"]
        if origin in allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            self.send_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, cls=CustomJSONEncoder, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _api_error(self, error: Exception) -> None:
        self._send_json({"error": str(error)}, 400)

    def _get_authenticated_session(self) -> dict[str, Any] | None:
        """Extract and verify Bearer token from Authorization header against Sessions table."""
        auth_header = self.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1].strip()
        return verify_session(token)

    def _require_auth(self, allowed_roles: list[str] | None = None) -> dict[str, Any] | None:
        """Enforce authentication and role permissions. Send 401/403 and return None if unauthorized."""
        session = self._get_authenticated_session()
        if not session:
            self._send_json({"error": "Unauthorized. Vui lòng đăng nhập để tiếp tục."}, 401)
            return None
        if allowed_roles and session.get("role") not in allowed_roles:
            self._send_json({"error": "Forbidden. Bạn không có quyền truy cập chức năng này."}, 403)
            return None
        return session

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        query = parse_qs(parsed_url.query)

        if endpoint == "/api/projects":
            try:
                broker_id = query.get("broker_id", [None])[0]
                if broker_id == 'broker_default':
                    session = self._get_authenticated_session()
                    if session and session['role'] == 'broker':
                        broker_id = session['user_id']
                    else:
                        broker_id = None
                include_inactive = query.get("include_inactive", ["0"])[0] in ("1", "true")
                self._send_json({"projects": list_projects(broker_id=broker_id, include_inactive=include_inactive)})
            except Exception as error:
                self._api_error(error)
            return
        elif endpoint == "/api/projects/sync-market":
            if not self._require_auth(allowed_roles=["admin"]): return
            try:
                self._send_json(sync_market_data())
            except Exception as error:
                self._api_error(error)
            return
        elif endpoint == "/api/broker/selection":
            session = self._require_auth(allowed_roles=["broker", "admin"])
            if not session: return
            try:
                broker_id = query.get("broker_id", [session["user_id"]])[0]
                self._send_json({"selected_project_ids": get_broker_selection(broker_id)})
            except Exception as error:
                self._api_error(error)
            return
        elif endpoint == "/api/users" or endpoint == "/api/admin/users":
            if not self._require_auth(allowed_roles=["admin"]): return
            try:
                self._send_json({"users": list_users(), "stats": get_system_stats()})
            except Exception as error:
                self._api_error(error)
            return
        elif endpoint == "/api/admin/system-stats":
            if not self._require_auth(allowed_roles=["admin"]): return
            try:
                self._send_json(get_system_stats())
            except Exception as error:
                self._api_error(error)
            return
        elif endpoint == "/api/clients":
            session = self._require_auth(allowed_roles=["broker", "admin"])
            if not session: return
            try:
                broker_id = query.get("broker_id", [session["user_id"]])[0]
                self._send_json({"clients": list_clients(broker_id=broker_id)})
            except Exception as error:
                self._api_error(error)
            return

        requested = ROOT / self.path.lstrip("/").split("?", 1)[0]
        if self.path != "/" and not requested.is_file():
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        endpoint = self.path.split("?", 1)[0]
        if not endpoint.startswith("/api/"):
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            client_ip = self.client_address[0] if self.client_address else "127.0.0.1"

            if endpoint == "/api/auth/login":
                self._send_json(authenticate_user(payload, client_ip=client_ip))
            elif endpoint == "/api/auth/logout":
                auth_header = self.headers.get("Authorization", "")
                token = auth_header.split(" ", 1)[1].strip() if "Bearer " in auth_header else ""
                if token:
                    revoke_session(token)
                self._send_json({"success": True, "message": "Đã đăng xuất thành công."})
            elif endpoint == "/api/analyze":
                self._send_json(analyze(payload))
            elif endpoint == "/api/clients":
                session = self._require_auth(allowed_roles=["broker", "admin"])
                if not session: return
                if "broker_id" not in payload:
                    payload["broker_id"] = session["user_id"]
                self._send_json({"client": create_client(payload)}, 201)
            elif endpoint == "/api/clients/delete":
                if not self._require_auth(allowed_roles=["broker", "admin"]): return
                cid = int(payload.get("client_id", 0))
                self._send_json(delete_client(cid))
            elif endpoint == "/api/projects/sync-market":
                if not self._require_auth(allowed_roles=["admin"]): return
                self._send_json(sync_market_data())
            elif endpoint == "/api/projects/parse-text":
                if not self._require_auth(allowed_roles=["admin", "broker"]): return
                self._send_json(parse_raw_project_text(payload.get("raw_text", "")))
            elif endpoint == "/api/projects":
                session = self._require_auth(allowed_roles=["admin", "broker"])
                if not session: return
                if session["role"] == "broker":
                    payload["broker_id"] = session["user_id"]
                self._send_json(create_or_update_project(payload))
            elif endpoint == "/api/projects/toggle":
                if not self._require_auth(allowed_roles=["admin"]): return
                pid = str(payload.get("project_id", ""))
                is_active = bool(payload.get("is_active", True))
                self._send_json(toggle_project_status(pid, is_active))
            elif endpoint == "/api/projects/delete":
                session = self._require_auth(allowed_roles=["admin", "broker"])
                if not session: return
                pid = str(payload.get("project_id", ""))
                self._send_json(delete_project(pid, role=session["role"], broker_id=session.get("user_id", "")))
            elif endpoint == "/api/broker/selection":
                session = self._require_auth(allowed_roles=["broker", "admin"])
                if not session: return
                broker_id = str(payload.get("broker_id", session["user_id"]))
                project_ids = list(payload.get("project_ids", []))
                self._send_json(save_broker_selection(broker_id, project_ids))
            elif endpoint == "/api/users":
                if not self._require_auth(allowed_roles=["admin"]): return
                self._send_json(save_user(payload))
            elif endpoint == "/api/users/toggle":
                if not self._require_auth(allowed_roles=["admin"]): return
                uid = str(payload.get("user_id", ""))
                self._send_json(toggle_user_status(uid))

            # ── Direct loan_dti.py endpoints ──────────────────────
            elif endpoint == "/api/simulate-loan":
                # Full loan simulation — returns complete amortization timeline
                profile = FinancialProfile(
                    monthly_income=decimal_value(payload.get("monthly_income", 65000000)),
                    available_cash=decimal_value(payload.get("available_cash", 1500000000)),
                    existing_debt_payment=decimal_value(payload.get("existing_debt_payment", 0)),
                    essential_expenses=decimal_value(payload.get("essential_expenses", 15000000)),
                    income_stability=str(payload.get("income_stability", "salaried")),
                )
                scenario = LoanScenario(
                    loan_ratio_percent=decimal_value(payload.get("loan_ratio_percent", 70)),
                    term_years=int(payload.get("term_years", 25)),
                    phase1_rate_percent=decimal_value(payload.get("phase1_rate_percent", 0)),
                    phase1_months=int(payload.get("phase1_months", 24)),
                    phase2_rate_percent=decimal_value(payload.get("phase2_rate_percent", 11)),
                    repayment_method=str(payload.get("repayment_method", "annuity")),
                    grace_type=str(payload.get("grace_type", "interest_only")),
                    grace_months=int(payload.get("grace_months", 24)),
                )
                project_price = decimal_value(payload.get("project_price", 5000000000))
                mgmt_fee = decimal_value(payload.get("monthly_management_fee", 0))

                analysis = simulate_loan(profile, scenario, project_price, mgmt_fee)

                # Serialize LoanAnalysis → JSON-safe dict
                timeline_rows = [
                    {
                        "month": r.month, "phase": r.phase,
                        "annual_rate_percent": float(r.annual_rate_percent),
                        "opening_balance": float(r.opening_balance),
                        "interest": float(r.interest),
                        "principal": float(r.principal),
                        "payment": float(r.payment),
                        "closing_balance": float(r.closing_balance),
                        "dti": float(r.dti),
                        "free_cash_flow": float(r.free_cash_flow),
                    }
                    for r in analysis.timeline
                ]
                shocks = [
                    {
                        "month": s.month,
                        "previous_payment": float(s.previous_payment),
                        "current_payment": float(s.current_payment),
                        "increase_ratio": float(s.increase_ratio) if s.increase_ratio is not None else None,
                    }
                    for s in analysis.payment_shocks
                ]
                self._send_json({
                    "initial_loan": float(analysis.initial_loan),
                    "ltv": float(analysis.ltv),
                    "max_payment": float(analysis.max_payment),
                    "max_payment_month": analysis.max_payment_month,
                    "max_dti": float(analysis.max_dti),
                    "max_dti_month": analysis.max_dti_month,
                    "min_fcf": float(analysis.min_fcf),
                    "min_fcf_month": analysis.min_fcf_month,
                    "survival_months": float(analysis.survival_months),
                    "illusion_of_safety": analysis.illusion_of_safety,
                    "hard_filter_reasons": list(analysis.hard_filter_reasons),
                    "is_eligible": analysis.is_eligible,
                    "timeline": timeline_rows,
                    "payment_shocks": shocks,
                    "dti_score": float(calculate_dti_score(analysis.max_dti)),
                    "ltv_score": float(calculate_ltv_score(analysis.ltv)),
                })

            elif endpoint == "/api/quick-calc":
                # Lightweight: just compute monthly payment (annuity) without full simulation
                balance = decimal_value(payload.get("loan_amount", 0))
                rate = decimal_value(payload.get("annual_rate_percent", 11))
                months = int(payload.get("term_months", 300))
                pmt = annuity_payment(balance, rate, months)
                self._send_json({
                    "monthly_payment": float(pmt),
                    "total_payment": float(pmt * months),
                    "total_interest": float(pmt * months - balance),
                    "loan_amount": float(balance),
                    "term_months": months,
                    "annual_rate_percent": float(rate),
                })

            else:
                self.send_error(404)
        except Exception as error:
            import traceback
            traceback.print_exc()
            self._api_error(error)

    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        if endpoint.startswith("/api/projects/"):
            if not self._require_auth(allowed_roles=["admin"]): return
            project_id = endpoint.split("/")[-1]
            try:
                self._send_json(delete_project(project_id))
            except Exception as error:
                self._api_error(error)
            return
        self.send_error(404)


if __name__ == "__main__":
    ThreadingHTTPServer.allow_reuse_address = True
    port = DEFAULT_PORT
    server = None
    
    for attempt in range(10):
        try:
            server = ThreadingHTTPServer((HOST, port), ReactRouterHandler)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                port += 1
            else:
                raise

    if server is None:
        raise RuntimeError("Không thể tìm thấy cổng mạng khả dụng để khởi chạy MinFit.")

    print(f"\n=======================================================")
    print(f"🚀 MinFit PropTech Web App đã sẵn sàng!")
    print(f"👉 Mở trình duyệt tại: http://localhost:{port}")
    print(f"👉 Hoặc địa chỉ IP:   http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ MinFit.")
        server.server_close()
