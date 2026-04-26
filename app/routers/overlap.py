from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.forms import OverlapInput, validate_form_data
from app.services.formatting import percent
from app.services.overlap_service import calculate_overlap

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/portfolio-overlap-checker", response_class=HTMLResponse)
async def overlap_page(request: Request):
    return templates.TemplateResponse("tools/overlap.html", _context(request))


@router.post("/portfolio-overlap-checker", response_class=HTMLResponse)
async def overlap_calculate(request: Request):
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(OverlapInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump())

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse("tools/overlap.html", context)

    result = calculate_overlap(data.first_portfolio, data.second_portfolio)
    result["overlap_percentage"] = percent(float(result["overlap_percentage"]))
    context["result"] = result
    return templates.TemplateResponse("tools/overlap.html", context)


def _context(request: Request, form: dict | None = None) -> dict:
    return {
        "request": request,
        "title": "Portfolio Overlap Tool | Free Portfolio Overlap Checker",
        "description": "Free portfolio overlap tool for comparing two stock name lists. Fast, private, and no login required.",
        "form": form or {
            "first_portfolio": "Reliance Industries\nTCS\nInfosys",
            "second_portfolio": "TCS\nHDFC Bank\nInfosys",
        },
    }

