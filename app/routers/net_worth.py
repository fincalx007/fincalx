"""Net Worth Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import NetWorthInput, validate_form_data
from app.services.net_worth_service import calculate_net_worth
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

DEFAULTS = {
    "total_assets": 500000,
    "total_liabilities": 200000,
}

PAGE_TITLE = "Net Worth Calculator India – Assets vs Liabilities"
PAGE_DESC = "Free net worth calculator India: estimate net worth by subtracting total liabilities from total assets."
TEMPLATE = "tools/net_worth.html"


@router.api_route(
    "/net-worth-calculator",
    response_class=HTMLResponse,
    name="net_worth_page",
    methods=["GET", "HEAD"],
)
async def net_worth_page(request: Request):

    return templates.TemplateResponse(TEMPLATE, _context(request))


@router.post("/net-worth-calculator", response_class=HTMLResponse, name="net_worth_calculate")
async def net_worth_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(NetWorthInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result_raw = calculate_net_worth(data.total_assets, data.total_liabilities)
    context["result"] = {
        "net_worth": money(result_raw["net_worth"]),
    }
    context["result_raw"] = result_raw
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/net-worth-calculator/api", name="net_worth_calculate_api")
async def net_worth_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "total_assets": _safe_float(raw_data.get("total_assets")),
            "total_liabilities": _safe_float(raw_data.get("total_liabilities")),
        }

        data, errors, error = validate_form_data(NetWorthInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_net_worth(data.total_assets, data.total_liabilities)
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

