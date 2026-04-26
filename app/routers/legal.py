from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["legal"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse(
        "legal/privacy.html",
        {
            "request": request,
            "title": "Privacy Policy | FinCalX India",
            "description": "Privacy policy for privacy-friendly finance calculators that do not require login or store calculator inputs.",
        },
    )


@router.get("/terms-of-service", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse(
        "legal/terms.html",
        {
            "request": request,
            "title": "Terms of Service | FinCalX India",
            "description": "Terms of service for educational SIP, EMI, income tax, and portfolio overlap calculators.",
        },
    )


@router.get("/disclaimer", response_class=HTMLResponse)
async def disclaimer(request: Request):
    return templates.TemplateResponse(
        "legal/disclaimer.html",
        {
            "request": request,
            "title": "Disclaimer | Not Financial Advice",
            "description": "Financial education disclaimer, SEBI registration notice, and calculation limitations for FinCalX India.",
        },
    )
