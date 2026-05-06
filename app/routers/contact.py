from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/contact", response_class=HTMLResponse, name="contact_page")
async def contact_page(request: Request):
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "title": "Contact FinCalX | Smart Financial Calculators",
            "description": "FinCalX provides free smart finance calculators. Contact us for feedback, suggestions, issue reporting, and business inquiries.",
        },
    )

