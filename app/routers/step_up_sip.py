"""Step-Up SIP Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import StepUpSIPInput, validate_form_data
from app.services.formatting import money
from app.services.step_up_sip_service import calculate_step_up_sip

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "monthly_investment": 5000,
    "annual_step_up_percentage": 10,
    "expected_annual_return": 12,
    "years": 10,
}

PAGE_TITLE = "Step-Up SIP Calculator India – Growing Monthly Investments"
PAGE_DESC = "Free step-up SIP calculator India: estimate total investment, wealth generated, and maturity value with annual step-up and expected returns."
TEMPLATE = "tools/step_up_sip.html"


@router.get("/step-up-sip-calculator", response_class=HTMLResponse, name="step_up_sip_page")
async def step_up_sip_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/step-up-sip-calculator", response_class=HTMLResponse, name="step_up_sip_calculate")
async def step_up_sip_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(StepUpSIPInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_step_up_sip(
        data.monthly_investment,
        data.annual_step_up_percentage,
        data.expected_annual_return,
        data.years,
    )

    context["result"] = {
        "total_investment": money(result_raw["total_invested"]),
        "wealth_generated": money(result_raw["wealth_generated"]),
        "maturity_value": money(result_raw["maturity_value"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/step-up-sip-calculator/api", name="step_up_sip_calculate_api")
async def step_up_sip_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "monthly_investment": _safe_float(raw_data.get("monthly_investment")),
            "annual_step_up_percentage": _safe_float(raw_data.get("annual_step_up_percentage")),
            "expected_annual_return": _safe_float(raw_data.get("expected_annual_return")),
            "years": _safe_int(raw_data.get("years")),
        }

        data, errors, error = validate_form_data(StepUpSIPInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_step_up_sip(
            data.monthly_investment,
            data.annual_step_up_percentage,
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

