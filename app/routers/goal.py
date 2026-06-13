"""Goal-Based Investment Calculator Router"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import GoalInput, validate_form_data
from app.services.formatting import money
from app.services.goal_service import calculate_goal_monthly

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "goal_amount": 1000000,
    "years": 5,
    "expected_annual_return": 8,
}

PAGE_TITLE = "Goal-Based Investment Calculator – Required Monthly SIP"
PAGE_DESC = "Calculate required monthly investment to reach a financial goal within a time horizon using expected returns."
TEMPLATE = "tools/goal.html"


@router.get("/goal-calculator", response_class=HTMLResponse, name="goal_page")
async def goal_page(request: Request):
    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/goal-calculator", response_class=HTMLResponse, name="goal_calculate")
async def goal_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(GoalInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_goal_monthly(data.goal_amount, data.years, data.expected_annual_return)

    context["result"] = {
        "required_monthly_investment": money(result_raw["required_monthly_investment"]),
        "total_invested": money(result_raw["total_invested"]),
        "expected_growth": money(result_raw["expected_growth"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/goal-calculator/api", name="goal_calculate_api")
async def goal_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "goal_amount": _safe_float(raw_data.get("goal_amount")),
            "years": _safe_int(raw_data.get("years")),
            "expected_annual_return": _safe_float(raw_data.get("expected_annual_return")),
        }

        data, errors, error = validate_form_data(GoalInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_goal_monthly(data.goal_amount, data.years, data.expected_annual_return)
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
