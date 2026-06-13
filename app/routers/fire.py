"""FIRE (Financial Independence Retire Early) Calculator Router

Follows the same architecture as other calculators.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import FIREInput, validate_form_data
from app.services.formatting import money
from app.services.fire_service import calculate_fire

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "annual_expenses": 600000,
    "safe_withdrawal_rate": 4,
}

PAGE_TITLE = "FIRE Calculator India – Estimate Your FIRE Number"
PAGE_DESC = "Estimate the FIRE number (required corpus) using your annual expenses and a safe withdrawal rate." 
TEMPLATE = "tools/fire.html"


@router.get("/fire-calculator", response_class=HTMLResponse, name="fire_page")
async def fire_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/fire-calculator", response_class=HTMLResponse, name="fire_calculate")
async def fire_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(FIREInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_fire(data.annual_expenses, data.safe_withdrawal_rate)

    context["result"] = {
        "fire_number": money(result_raw["fire_number"]),
        "required_retirement_corpus": money(result_raw["required_retirement_corpus"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/fire-calculator/api", name="fire_calculate_api")
async def fire_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "annual_expenses": _safe_float(raw_data.get("annual_expenses")),
            "safe_withdrawal_rate": _safe_float(raw_data.get("safe_withdrawal_rate")),
        }

        data, errors, error = validate_form_data(FIREInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_fire(data.annual_expenses, data.safe_withdrawal_rate)
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


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": PAGE_TITLE,
        "description": PAGE_DESC,
        "form": form or DEFAULTS.copy(),
    }
