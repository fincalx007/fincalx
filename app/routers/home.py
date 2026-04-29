from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    tools = [
        {
            "title": "SIP Calculator",
            "description": "Estimate SIP maturity amount, invested value, and projected returns.",
            "href": "/tools/sip-calculator",
            "keywords": "sip calculator india",
            "icon": "SIP",
        },
        {
            "title": "EMI Calculator",
            "description": "Calculate monthly EMI, total interest, and total repayment.",
            "href": "/tools/emi-calculator",
            "keywords": "emi calculator",
            "icon": "EMI",
        },
        {
            "title": "Salary Calculator",
            "description": "Calculate monthly and annual in-hand salary from CTC with PF and tax breakdown.",
            "href": "/tools/salary-calculator",
            "keywords": "salary calculator india in hand salary calculator ctc to in hand salary",
            "icon": "SALARY",
        },
        {
            "title": "Portfolio Overlap Checker",
            "description": "Check common stock names across two simple portfolios.",
            "href": "/tools/portfolio-overlap-checker",
            "keywords": "portfolio overlap checker",
            "icon": "PO",
        },
    ]
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "SIP Calculator India | EMI & Tax Calculator",
            "description": "Free SIP, EMI, and Income Tax calculators for India. Fast, accurate, and no login required.",
            "tools": tools,
        },
    )
