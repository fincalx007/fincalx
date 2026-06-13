"""CAGR Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import CAGRInput, validate_form_data
from app.services.cagr_service import calculate_cagr
from app.services.formatting import percent

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

# Default form values
DEFAULTS = {
    "initial_investment": 100000,
    "final_value": 200000,
    "years": 5,
}

PAGE_TITLE = "CAGR Calculator India – Annualized Growth Rate"
PAGE_DESC = "Free CAGR calculator India: estimate compound annual growth rate using initial investment, final value, and investment years."
TEMPLATE = "tools/cagr.html"


@router.get("/cagr-calculator", response_class=HTMLResponse, name="cagr_page")
async def cagr_page(request: Request):
    """Render CAGR calculator page."""
    return templates.TemplateResponse(
        TEMPLATE,
        _context(request),
    )


@router.post("/cagr-calculator", response_class=HTMLResponse, name="cagr_calculate")
async def cagr_calculate(request: Request):
    """Process CAGR calculation."""
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(CAGRInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_cagr(data.initial_investment, data.final_value, data.years)
    context["result"] = {"cagr": percent(result_raw["cagr"]) }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/cagr-calculator/api", name="cagr_calculate_api")
async def cagr_calculate_api(request: Request):
    """Process CAGR calculation for AJAX clients."""
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "initial_investment": _safe_float(raw_data.get("initial_investment")),
            "final_value": _safe_float(raw_data.get("final_value")),
            "years": _safe_int(raw_data.get("years")),
        }

        data, errors, error = validate_form_data(CAGRInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_cagr(data.initial_investment, data.final_value, data.years)
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
    """Build page context."""
    return {
        "request": request,
        "title": PAGE_TITLE,
        "description": PAGE_DESC,
        "form": form or DEFAULTS.copy(),
    }

