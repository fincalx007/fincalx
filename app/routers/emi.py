"""
EMI Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import EMIInput, validate_form_data
from app.services.emi_service import calculate_emi
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

# Default form values
DEFAULTS = {
    "loan_amount": 1000000,
    "annual_rate": 8.5,
    "years": 20,
}

PAGE_TITLE = "EMI Calculator India – Loan EMI & Interest Calculator"
PAGE_DESC = "Free EMI calculator India: calculate home, car & personal loan EMI, total interest & repayment in seconds. Compare lenders privately & plan your budget."
TEMPLATE = "tools/emi.html"


@router.get("/emi-calculator", response_class=HTMLResponse, name="emi_page")
async def emi_page(request: Request):
    """Render EMI calculator page."""
    return templates.TemplateResponse(
        TEMPLATE,
        _context(request),
    )


@router.post("/emi-calculator", response_class=HTMLResponse, name="emi_calculate")
async def emi_calculate(request: Request):
    """Process EMI calculation."""
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(EMIInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result = calculate_emi(data.loan_amount, data.annual_rate, data.years)
    context["result"] = {key: money(value) for key, value in result.items()}
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/emi-calculator/api", name="emi_calculate_api")
async def emi_calculate_api(request: Request):
    """Process EMI calculation for AJAX clients."""
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        data, errors, error = validate_form_data(
            EMIInput,
            {
                "loan_amount": _safe_float(raw_data.get("loan_amount")),
                "annual_rate": _safe_float(raw_data.get("annual_rate")),
                "years": _safe_int(raw_data.get("years")),
            },
        )

        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_emi(data.loan_amount, data.annual_rate, data.years)
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
