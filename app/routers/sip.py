"""
SIP Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import SIPInput, validate_form_data
from app.services.formatting import money
from app.services.sip_service import calculate_sip

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

# Default form values
DEFAULTS = {
    "monthly_investment": 5000,
    "annual_rate": 12,
    "years": 10,
}

PAGE_TITLE = "SIP Calculator India 2026 – Calculate Returns & Investment Growth"
PAGE_DESC = "Free SIP calculator India 2026: plan monthly mutual fund investments, estimate maturity amount & compare returns. Private, fast & accurate."
TEMPLATE = "tools/sip.html"


@router.get("/sip-calculator", response_class=HTMLResponse, name="sip_page")
async def sip_page(request: Request):
    """Render SIP calculator page."""
    return templates.TemplateResponse(
        TEMPLATE,
        _context(request),
    )


@router.post("/sip-calculator", response_class=HTMLResponse, name="sip_calculate")
async def sip_calculate(request: Request):
    """Process SIP calculation."""
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(SIPInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result = calculate_sip(data.monthly_investment, data.annual_rate, data.years)
    context["result"] = {key: money(value) for key, value in result.items()}
    context["result_raw"] = result
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/sip-calculator/api", name="sip_calculate_api")
async def sip_calculate_api(request: Request):
    """Process SIP calculation for AJAX clients."""
    try:
        try:
            data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        print("INPUT:", data)

        if not isinstance(data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "monthly_investment": _safe_float(data.get("monthly_investment")),
            "annual_rate": _safe_float(data.get("annual_rate")),
            "years": _safe_int(data.get("years")),
        }

        data_model, errors, error = validate_form_data(SIPInput, cleaned)
        if errors or not data_model:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_sip(data_model.monthly_investment, data_model.annual_rate, data_model.years)
        print("RESULT:", result)

        return JSONResponse(
            {
                "total_value": result["maturity_amount"],
                "invested_amount": result["total_invested"],
                "estimated_returns": result["returns"],
            }
        )
    except Exception as exc:
        print("RESULT:", {"error": str(exc)})
        return JSONResponse({"error": "Calculation failed. Please try again."}, status_code=200)


def _safe_float(value):
    """Convert JSON input to float while treating empty values as invalid."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_int(value):
    """Convert JSON input to int while treating empty values as invalid."""
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
