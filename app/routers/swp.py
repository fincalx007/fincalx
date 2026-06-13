"""SWP (Systematic Withdrawal Plan) Calculator Router

Follows patterns used by existing calculators (SIP, Lumpsum, CAGR).
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import SWPInput, validate_form_data
from app.services.formatting import money
from app.services.swp_service import calculate_swp

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "initial_corpus": 1000000,
    "monthly_withdrawal": 20000,
    "expected_annual_return": 6,
    "years": 10,
}

PAGE_TITLE = "SWP Calculator India – Systematic Withdrawal Plan Estimate"
PAGE_DESC = "Free SWP calculator India: estimate remaining corpus, total withdrawals, and corpus growth under a monthly withdrawal plan."
TEMPLATE = "tools/swp.html"


@router.get("/swp-calculator", response_class=HTMLResponse, name="swp_page")
async def swp_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/swp-calculator", response_class=HTMLResponse, name="swp_calculate")
async def swp_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(SWPInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_swp(
        data.initial_corpus,
        data.monthly_withdrawal,
        data.expected_annual_return,
        data.years,
    )

    context["result"] = {
        "remaining_corpus": money(result_raw["remaining_corpus"]),
        "total_withdrawals": money(result_raw["total_withdrawals"]),
        "corpus_growth": money(result_raw["corpus_growth"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/swp-calculator/api", name="swp_calculate_api")
async def swp_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "initial_corpus": _safe_float(raw_data.get("initial_corpus")),
            "monthly_withdrawal": _safe_float(raw_data.get("monthly_withdrawal")),
            "expected_annual_return": _safe_float(raw_data.get("expected_annual_return")),
            "years": _safe_int(raw_data.get("years")),
        }

        data, errors, error = validate_form_data(SWPInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_swp(
            data.initial_corpus,
            data.monthly_withdrawal,
            data.expected_annual_return,
            data.years,
        )
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
