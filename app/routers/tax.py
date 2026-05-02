from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import TaxInput, validate_form_data
from app.services.formatting import money
from app.services.tax_service import calculate_income_tax

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "Income Tax Calculator India FY 2025-26",
        "description": "Calculate income tax instantly.",
        "form": form or {
            "gross_income": 1200000,
            "regime": "new",
            "deductions": 0,
        },
    }


@router.get("/income-tax-calculator", response_class=HTMLResponse)
async def tax_page(request: Request):
    return templates.TemplateResponse("tools/tax.html", _context(request))


@router.post("/income-tax-calculator", response_class=HTMLResponse)
async def tax_calculate(request: Request):
    raw_form = dict(await request.form())

    for key in ("gross_income", "deductions"):
        val = raw_form.get(key)
        if val is not None:
            raw_form[key] = str(val).replace(",", "")

    try:
        data = TaxInput(**raw_form)
        errors = None
        error = None
    except Exception:
        data = None
        errors = True
        error = "Invalid input. Please check your values."

    context = _context(request, form=raw_form)

    if errors:
        context["error"] = error
        return templates.TemplateResponse("tools/tax.html", context)

    try:
        result = calculate_income_tax(
            data.gross_income,
            data.regime,
            data.deductions,
        )
    except Exception:
        context["error"] = "Calculation failed. Please try again."
        return templates.TemplateResponse("tools/tax.html", context)

    context["result"] = {
        "regime": result.get("regime"),
        "taxable_income": money(result.get("taxable_income", 0)),
        "base_tax": money(result.get("base_tax", 0)),
        "cess": money(result.get("cess", 0)),
        "total_tax": money(result.get("total_tax", 0)),
        "surcharge": money(result.get("surcharge", 0)),
    }

    return templates.TemplateResponse("tools/tax.html", context)


@router.post("/income-tax-calculator/api")
async def tax_calculate_api(request: Request):
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        cleaned = {
            "gross_income": _safe_float(raw_data.get("gross_income")),
            "regime": raw_data.get("regime"),
            "deductions": _safe_float(raw_data.get("deductions")),
        }

        data, errors, error = validate_form_data(TaxInput, cleaned)
        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_income_tax(data.gross_income, data.regime, data.deductions)
        return JSONResponse(
            {
                "regime": result.get("regime"),
                "taxable_income": result.get("taxable_income", 0),
                "base_tax": result.get("base_tax", 0),
                "cess": result.get("cess", 0),
                "total_tax": result.get("total_tax", 0),
                "surcharge": result.get("surcharge", 0),
            }
        )
    except Exception:
        return JSONResponse({"error": "Calculation failed. Please try again."}, status_code=200)


def _safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
