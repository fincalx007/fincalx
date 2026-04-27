from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.forms import SIPInput, validate_form_data
from app.services.formatting import money
from app.services.sip_service import calculate_sip

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/sip-calculator", response_class=HTMLResponse)
async def sip_page(request: Request):
    return templates.TemplateResponse("tools/sip.html", _context(request))


@router.post("/sip-calculator", response_class=HTMLResponse)
async def sip_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(SIPInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/sip.html", context)

    result = calculate_sip(data.monthly_investment, data.annual_rate, data.years)
    context["result"] = {key: money(value) for key, value in result.items()}
    context["result_raw"] = result
    return templates.TemplateResponse("tools/sip.html", context)


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "SIP Calculator India 2026 – Calculate Returns & Investment Growth",
        "description": "Free SIP calculator India 2026: plan monthly mutual fund investments, estimate maturity amount & compare returns. Private, fast & accurate.",
        "form": form or {"monthly_investment": 5000, "annual_rate": 12, "years": 10},
    }
