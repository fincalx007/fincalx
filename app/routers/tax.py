from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.forms import TaxInput, validate_form_data
from app.services.formatting import money
from app.services.tax_service import calculate_income_tax

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/income-tax-calculator", response_class=HTMLResponse)
async def tax_page(request: Request):
    return templates.TemplateResponse("tools/tax.html", _context(request))


@router.post("/income-tax-calculator", response_class=HTMLResponse)
async def tax_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(TaxInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/tax.html", context)

    result = calculate_income_tax(data.gross_income, data.regime, data.deductions)
    context["result"] = {
        "regime": result["regime"],
        "taxable_income": money(float(result["taxable_income"])),
        "base_tax": money(float(result["base_tax"])),
        "cess": money(float(result["cess"])),
        "total_tax": money(float(result["total_tax"])),
    }
    return templates.TemplateResponse("tools/tax.html", context)


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "Income Tax Calculator India FY 2025-26 (Updated 2026) | Old vs New Regime",
        "description": "Free income tax calculator India FY 2025-26: compare old vs new regime, estimate tax liability, cess & take-home salary. Updated for latest slabs.",
        "last_updated": "April 2026 (FY 2025-26)",
        "last_modified_iso": "2026-04-01",
        "form": form or {"gross_income": 1200000, "regime": "new", "deductions": 0},
    }
