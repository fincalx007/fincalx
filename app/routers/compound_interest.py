"""Compound Interest Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import CompoundInterestInput, validate_form_data
from app.services.compound_interest_service import calculate_compound_interest
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "principal_amount": 100000,
    "interest_rate": 10,
    "time_period_years": 5,
    "compounding_frequency": 12,
}

PAGE_TITLE = "Compound Interest Calculator India – Growth & Returns"
PAGE_DESC = "Free compound interest calculator India: estimate interest earned and maturity value with a chosen compounding frequency."
TEMPLATE = "tools/compound_interest.html"


@router.api_route(
    "/compound-interest-calculator",
    response_class=HTMLResponse,
    name="compound_interest_page",
    methods=["GET", "HEAD"],
)
async def compound_interest_page(request: Request):

    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/compound-interest-calculator", response_class=HTMLResponse, name="compound_interest_calculate")
async def compound_interest_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(CompoundInterestInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_compound_interest(
        data.principal_amount,
        data.interest_rate,
        data.time_period_years,
        data.compounding_frequency,
    )
    context["result"] = {
        "interest_earned": money(result_raw["interest_earned"]),
        "maturity_value": money(result_raw["maturity_value"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/compound-interest-calculator/api", name="compound_interest_calculate_api")
async def compound_interest_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "principal_amount": _safe_float(raw_data.get("principal_amount")),
            "interest_rate": _safe_float(raw_data.get("interest_rate")),
            "time_period_years": _safe_int(raw_data.get("time_period_years")),
            "compounding_frequency": _safe_int(raw_data.get("compounding_frequency")),
        }

        data, errors, error = validate_form_data(CompoundInterestInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_compound_interest(
            data.principal_amount,
            data.interest_rate,
            data.time_period_years,
            data.compounding_frequency,
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

