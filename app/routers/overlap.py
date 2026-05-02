"""
Portfolio Overlap Checker Router

Standardized calculator with consistent pattern.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.forms import OverlapInput, validate_form_data
from app.services.formatting import percent
from app.services.overlap_service import calculate_overlap

router = APIRouter(prefix="/tools", tags=["tools"])
templates = Jinja2Templates(directory="app/templates")

# Default form values
DEFAULTS = {
    "first_portfolio": "Reliance Industries\nTCS\nInfosys",
    "second_portfolio": "TCS\nHDFC Bank\nInfosys",
}

PAGE_TITLE = "Portfolio Overlap Checker – Compare Mutual Fund Holdings"
PAGE_DESC = "Free portfolio overlap checker: compare mutual fund holdings & stock portfolios instantly. Reduce duplication, improve diversification & invest smarter."
TEMPLATE = "tools/overlap.html"


@router.get("/portfolio-overlap-checker", response_class=HTMLResponse, name="overlap_page")
async def overlap_page(request: Request):
    """Render overlap checker page."""
    return templates.TemplateResponse(
        TEMPLATE,
        _context(request),
    )


@router.post("/portfolio-overlap-checker", response_class=HTMLResponse, name="overlap_calculate")
async def overlap_calculate(request: Request):
    """Process overlap calculation."""
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(OverlapInput, raw_form)

    context = _context(request, form=raw_form if errors else data.model_dump() if data else None)

    if errors:
        context["errors"] = errors
        context["error"] = error
        return templates.TemplateResponse(TEMPLATE, context)

    result = calculate_overlap(data.first_portfolio, data.second_portfolio)
    result["overlap_percentage"] = percent(float(result["overlap_percentage"]))
    context["result"] = result
    return templates.TemplateResponse(TEMPLATE, context)


@router.post("/portfolio-overlap-checker/api", name="overlap_calculate_api")
async def overlap_calculate_api(request: Request):
    """Process portfolio overlap calculation for AJAX clients."""
    try:
        try:
            raw_data = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON request."}, status_code=400)

        if not isinstance(raw_data, dict):
            return JSONResponse({"error": "Invalid input data."}, status_code=400)

        data, errors, error = validate_form_data(
            OverlapInput,
            {
                "first_portfolio": raw_data.get("first_portfolio") or "",
                "second_portfolio": raw_data.get("second_portfolio") or "",
            },
        )

        if errors or not data:
            return JSONResponse({"error": error or "Please check your inputs and try again."}, status_code=400)

        result = calculate_overlap(data.first_portfolio, data.second_portfolio)
        return JSONResponse(result)
    except Exception:
        return JSONResponse({"error": "Calculation failed. Please try again."}, status_code=200)


def _context(request: Request, form: dict | None = None) -> dict:
    """Build page context."""
    return {
        "request": request,
        "title": PAGE_TITLE,
        "description": PAGE_DESC,
        "form": form or DEFAULTS.copy(),
    }
