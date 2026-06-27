"""Inflation Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import InflationInput, validate_form_data
from app.services.inflation_service import calculate_inflation_future_value
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "current_amount": 100000,
    "inflation_rate": 6,
    "number_of_years": 10,
}

PAGE_TITLE = "Inflation Calculator India – Future Value & Power Impact"
PAGE_DESC = "Free inflation calculator India: estimate future value and purchasing power impact over years given an inflation rate."
TEMPLATE = "tools/inflation.html"


@router.api_route(
    "/inflation-calculator",
    response_class=HTMLResponse,
    name="inflation_page",
    methods=["GET", "HEAD"],
)
async def inflation_page(request: Request):

    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/inflation-calculator", response_class=HTMLResponse, name="inflation_calculate")
async def inflation_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(InflationInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_inflation_future_value(data.current_amount, data.inflation_rate, data.number_of_years)
    context["result"] = {
        "future_value": money(result_raw["future_value"]),
        "purchasing_power_impact": money(result_raw["purchasing_power_impact"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/inflation-calculator/api", name="inflation_calculate_api")
async def inflation_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "current_amount": _safe_float(raw_data.get("current_amount")),
            "inflation_rate": _safe_float(raw_data.get("inflation_rate")),
            "number_of_years": _safe_int(raw_data.get("number_of_years")),
        }

        data, errors, error = validate_form_data(InflationInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_inflation_future_value(data.current_amount, data.inflation_rate, data.number_of_years)
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

