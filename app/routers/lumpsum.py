"""Lumpsum Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import LumpsumInput, validate_form_data
from app.services.lumpsum_service import calculate_lumpsum
from app.services.formatting import money, percent

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "investment_amount": 100000,
    "expected_annual_return": 12,
    "investment_duration_years": 5,
}

PAGE_TITLE = "Lumpsum Calculator India – Maturity & Returns"
PAGE_DESC = "Free lumpsum calculator India: estimate maturity value and estimated returns from an initial investment at an expected annual return."
TEMPLATE = "tools/lumpsum.html"


@router.get("/lumpsum-calculator", response_class=HTMLResponse, name="lumpsum_page")
async def lumpsum_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/lumpsum-calculator", response_class=HTMLResponse, name="lumpsum_calculate")
async def lumpsum_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(LumpsumInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_lumpsum(data.investment_amount, data.expected_annual_return, data.investment_duration_years)
    context["result"] = {
        "invested_amount": money(result_raw["invested_amount"]),
        "estimated_returns": money(result_raw["estimated_returns"]),
        "maturity_value": money(result_raw["maturity_value"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/lumpsum-calculator/api", name="lumpsum_calculate_api")
async def lumpsum_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "investment_amount": _safe_float(raw_data.get("investment_amount")),
            "expected_annual_return": _safe_float(raw_data.get("expected_annual_return")),
            "investment_duration_years": _safe_int(raw_data.get("investment_duration_years")),
        }

        data, errors, error = validate_form_data(LumpsumInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_lumpsum(data.investment_amount, data.expected_annual_return, data.investment_duration_years)
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

