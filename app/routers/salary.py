from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.forms import SalaryInput, validate_form_data
from app.services.formatting import money
from app.services.salary_service import calculate_salary

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/salary-calculator", response_class=HTMLResponse)
async def salary_page(request: Request):
    return templates.TemplateResponse("tools/salary.html", _context(request))


@router.post("/salary-calculator", response_class=HTMLResponse)
async def salary_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(SalaryInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/salary.html", context)

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
    return templates.TemplateResponse("tools/salary.html", context)


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "Salary Calculator India 2026 – In-hand Salary from CTC",
        "description": "Calculate your in-hand salary from CTC instantly. Free salary calculator India with PF, tax, and monthly breakdown.",
        "form": form
        or {
            "ctc": 1200000,
            "basic_pct": 40,
            "hra_pct": 20,
            "other_allowances": 0,
            "pf_pct": 12,
            "tax_pct": 10,
        },
    }

