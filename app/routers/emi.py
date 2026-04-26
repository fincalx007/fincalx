from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.forms import EMIInput, validate_form_data
from app.services.emi_service import calculate_emi
from app.services.formatting import money

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/emi-calculator", response_class=HTMLResponse)
async def emi_page(request: Request):
    return templates.TemplateResponse("tools/emi.html", _context(request))


@router.post("/emi-calculator", response_class=HTMLResponse)
async def emi_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(EMIInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/emi.html", context)

    result = calculate_emi(data.loan_amount, data.annual_rate, data.years)
    context["result"] = {key: money(value) for key, value in result.items()}
    return templates.TemplateResponse("tools/emi.html", context)


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "EMI Calculator India | Free Loan EMI Calculator",
        "description": "Free EMI calculator for monthly loan instalment, total interest, and total repayment estimates. Fast, private, and no login required.",
        "form": form or {"loan_amount": 1000000, "annual_rate": 8.5, "years": 20},
    }
