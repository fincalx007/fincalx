"""
Salary Calculator Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import SalaryInput, validate_form_data
from app.services.formatting import money
from app.services.salary_service import calculate_salary

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

# Default form values
DEFAULTS = {
    "ctc": 1200000,
    "basic_pct": 40,
    "hra_pct": 20,
    "other_allowances": 0,
    "pf_pct": 12,
    "tax_pct": 10,
}

PAGE_TITLE = "Salary Calculator India 2026 – In-hand Salary from CTC"
PAGE_DESC = "Calculate your in-hand salary from CTC instantly. Free salary calculator India with PF, tax, and monthly breakdown."
TEMPLATE = "tools/salary.html"


@router.get("/salary-calculator", response_class=HTMLResponse, name="salary_page")
async def salary_page(request: Request):
    """Render salary calculator page."""
    return templates.TemplateResponse(
        TEMPLATE,
        _context(request),
    )


@router.post("/salary-calculator", response_class=HTMLResponse, name="salary_calculate")
async def salary_calculate(request: Request):
    """Process salary calculation."""
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(SalaryInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result = calculate_salary(
        data.ctc,
        data.basic_pct,
        data.hra_pct,
        data.other_allowances,
        data.pf_pct,
        data.tax_pct,
    )
    context["result"] = {key: money(value) for key, value in result.items()}
    context["result_raw"] = result
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/salary-calculator/api", name="salary_calculate_api")
async def salary_calculate_api(request: Request):
    """Process salary calculation for AJAX clients."""
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        data, errors, error = validate_form_data(
            SalaryInput,
            {
                "ctc": _safe_float(raw_data.get("ctc")),
                "basic_pct": _safe_float(raw_data.get("basic_pct")),
                "hra_pct": _safe_float(raw_data.get("hra_pct")),
                "other_allowances": _safe_float(raw_data.get("other_allowances")),
                "pf_pct": _safe_float(raw_data.get("pf_pct")),
                "tax_pct": _safe_float(raw_data.get("tax_pct")),
            },
        )

        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_salary(
            data.ctc,
            data.basic_pct,
            data.hra_pct,
            data.other_allowances,
            data.pf_pct,
            data.tax_pct,
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


def _context(request: Request, form: dict | None = None) -> dict:
    """Build page context."""
    return {
        "request": request,
        "title": PAGE_TITLE,
        "description": PAGE_DESC,
        "form": form or DEFAULTS.copy(),
    }
