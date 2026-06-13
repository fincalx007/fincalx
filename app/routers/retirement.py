"""Retirement Calculator Router

Follows patterns used by other calculators.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import RetirementInput, validate_form_data
from app.services.formatting import money
from app.services.retirement_service import calculate_retirement_corpus

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "current_age": 30,
    "retirement_age": 60,
    "current_savings": 500000,
    "monthly_investment": 5000,
    "expected_annual_return": 8,
}

PAGE_TITLE = "Retirement Calculator India – Plan Retirement Corpus & Income"
PAGE_DESC = "Estimate retirement corpus and potential retirement income using current savings, monthly investments, and expected returns."
TEMPLATE = "tools/retirement.html"


@router.get("/retirement-calculator", response_class=HTMLResponse, name="retirement_page")
async def retirement_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/retirement-calculator", response_class=HTMLResponse, name="retirement_calculate")
async def retirement_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(RetirementInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_retirement_corpus(
        data.current_age,
        data.retirement_age,
        data.current_savings,
        data.monthly_investment,
        data.expected_annual_return,
    )

    context["result"] = {
        "retirement_corpus": money(result_raw["retirement_corpus"]),
        "estimated_annual_income": money(result_raw["estimated_annual_income"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/retirement-calculator/api", name="retirement_calculate_api")
async def retirement_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "current_age": _safe_int(raw_data.get("current_age")),
            "retirement_age": _safe_int(raw_data.get("retirement_age")),
            "current_savings": _safe_float(raw_data.get("current_savings")),
            "monthly_investment": _safe_float(raw_data.get("monthly_investment")),
            "expected_annual_return": _safe_float(raw_data.get("expected_annual_return")),
        }

        data, errors, error = validate_form_data(RetirementInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_retirement_corpus(
            data.current_age,
            data.retirement_age,
            data.current_savings,
            data.monthly_investment,
            data.expected_annual_return,
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
