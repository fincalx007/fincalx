"""Emergency Fund Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import EmergencyFundInput, validate_form_data
from app.services.emergency_fund_service import calculate_emergency_fund
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "monthly_expenses": 50000,
    "emergency_coverage_months": 6,
}

PAGE_TITLE = "Emergency Fund Calculator India – Recommended Safety Buffer"
PAGE_DESC = "Free emergency fund calculator India: estimate recommended emergency fund using your monthly expenses and coverage months."
TEMPLATE = "tools/emergency_fund.html"


@router.get("/emergency-fund-calculator", response_class=HTMLResponse, name="emergency_fund_page")
async def emergency_fund_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/emergency-fund-calculator", response_class=HTMLResponse, name="emergency_fund_calculate")
async def emergency_fund_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(EmergencyFundInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_emergency_fund(data.monthly_expenses, data.emergency_coverage_months)
    context["result"] = {
        "recommended_emergency_fund": money(result_raw["recommended_emergency_fund"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/emergency-fund-calculator/api", name="emergency_fund_calculate_api")
async def emergency_fund_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "monthly_expenses": _safe_float(raw_data.get("monthly_expenses")),
            "emergency_coverage_months": _safe_int(raw_data.get("emergency_coverage_months")),
        }

        data, errors, error = validate_form_data(EmergencyFundInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_emergency_fund(data.monthly_expenses, data.emergency_coverage_months)
        return JSONResponse(result)
    except Exception:
        return JSONResponse({"error": "Calculation failed. Please try again."}, status_code=200)


def _safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value):
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": PAGE_TITLE,
        "description": PAGE_DESC,
        "form": form or DEFAULTS.copy(),
    }

