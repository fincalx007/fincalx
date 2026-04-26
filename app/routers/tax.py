from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
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

    # Remove commas safely
    for key in ("gross_income", "deductions"):
        val = raw_form.get(key)
        if val is not None:
            raw_form[key] = str(val).replace(",", "")

    data, errors, error = validate_form_data(TaxInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/tax.html", context)

    result = calculate_income_tax(
        data.gross_income,
        data.regime,
        data.deductions,
    )

    context["result"] = {
        "regime": result["regime"],
        "taxable_income": money(result["taxable_income"]),
        "base_tax": money(result["base_tax"]),
        "cess": money(result["cess"]),
        "total_tax": money(result["total_tax"]),
        "surcharge": money(result["surcharge"]),
    }

    return templates.TemplateResponse("tools/tax.html", context)

