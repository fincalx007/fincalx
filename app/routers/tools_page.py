from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.evergreen_calculator_service import calculator_cards

router = APIRouter(prefix="/tools", tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse, name="tools_index")
async def tools_index(request: Request):
    return templates.TemplateResponse(
        "tools_page.html",
        {
            "request": request,
            "title": "All Tools | FinCalX",
            "description": "Browse all FinCalX calculators grouped by category.",
            "evergreen_calculators": calculator_cards(),
        },
    )
