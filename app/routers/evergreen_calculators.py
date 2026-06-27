from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.evergreen_calculator_service import (
    EVERGREEN_CALCULATORS,
    calculate,
    defaults_for,
    educational_sections,
    faqs_for,
    related_calculators,
    validate_inputs,
)
from app.services.formatting import money, percent

router = APIRouter(prefix="/tools", tags=["evergreen-tools"])
templates = Jinja2Templates(directory="app/templates")
TEMPLATE = "tools/evergreen_calculator.html"

PERCENT_KEYS = {
    "savings_rate",
    "debt_to_income_ratio",
    "real_rate_of_return",
    "portfolio_return",
    "equity_allocation",
    "debt_allocation",
    "cash_allocation",
    "other_allocation",
}

COUNT_KEYS = {
    "estimated_years_to_double",
    "months_to_payoff",
    "years_to_payoff",
    "months_to_target",
    "years_to_target",
    "new_months_to_payoff",
    "total_quantity",
}


def _format_value(key: str, value: float) -> str:
    if key in PERCENT_KEYS:
        return percent(value)
    if key in COUNT_KEYS:
        return f"{value:,.2f}".rstrip("0").rstrip(".")
    return money(value)


def _format_result(result: dict[str, float]) -> dict[str, str]:
    return {key: _format_value(key, value) for key, value in result.items()}


def _context(request: Request, calculator, form: dict | None = None, result: dict | None = None, error: str | None = None) -> dict:
    raw_result = result or {}
    return {
        "request": request,
        "title": f"{calculator.title} | FinCalX",
        "description": calculator.description,
        "calculator": calculator,
        "form": form or defaults_for(calculator),
        "result": _format_result(raw_result) if raw_result else None,
        "result_raw": raw_result,
        "result_labels": calculator.result_labels,
        "sections": educational_sections(calculator),
        "faqs": faqs_for(calculator),
        "related_calculators": related_calculators(calculator),
        "error": error,
    }


def _register_calculator(calculator):
    async def page(request: Request):
        return templates.TemplateResponse(TEMPLATE, _context(request, calculator))

    async def submit(request: Request):
        raw_form = dict(await request.form())
        values, error = validate_inputs(calculator, raw_form)
        if error or values is None:
            return templates.TemplateResponse(TEMPLATE, _context(request, calculator, form=raw_form, error=error))
        result = calculate(calculator, values)
        return templates.TemplateResponse(TEMPLATE, _context(request, calculator, form=values, result=result))

    async def api(request: Request):
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)
        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)
        values, error = validate_inputs(calculator, raw_data)
        if error or values is None:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)
        return JSONResponse(calculate(calculator, values))

    route = f"/{calculator.slug}"
    router.add_api_route(route, page, methods=["GET", "HEAD"], response_class=HTMLResponse, name=f"{calculator.key}_page")
    router.add_api_route(route, submit, methods=["POST"], response_class=HTMLResponse, name=f"{calculator.key}_calculate")
    router.add_api_route(f"{route}/api", api, methods=["POST"], name=f"{calculator.key}_api")


for _calculator in EVERGREEN_CALCULATORS:
    _register_calculator(_calculator)
