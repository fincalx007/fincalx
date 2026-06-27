from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.api_route("/", response_class=HTMLResponse, methods=["GET", "HEAD"])
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
        {
            "title": "CAGR Calculator",
            "description": "Estimate annualized growth rate between an initial investment and final value.",
            "href": "/tools/cagr-calculator",
            "keywords": "cagr calculator compound annual growth rate",
            "icon": "CAGR",
        },
        {
            "title": "Step-Up SIP Calculator",
            "description": "Estimate maturity value with a growing SIP contribution pattern based on an annual step-up.",
            "href": "/tools/step-up-sip-calculator",
            "keywords": "step-up sip calculator step up sip monthly investment annual step-up expected return",
            "icon": "SIP",
        },
        {
            "title": "SWP Calculator",
            "description": "Estimate remaining corpus and total withdrawals from a systematic withdrawal plan.",
            "href": "/tools/swp-calculator",
            "keywords": "swp calculator systematic withdrawal plan remaining corpus withdrawals",
            "icon": "SWP",
        },
        {
            "title": "Retirement Calculator",
            "description": "Estimate retirement corpus and potential retirement income.",
            "href": "/tools/retirement-calculator",
            "keywords": "retirement calculator retirement corpus estimated income",
            "icon": "RET",
        },
        {
            "title": "FIRE Calculator",
            "description": "Estimate FIRE number and required retirement corpus using safe withdrawal rate.",
            "href": "/tools/fire-calculator",
            "keywords": "fire calculator financial independence retire early",
            "icon": "FIRE",
        },
        {
            "title": "Goal-Based Investment Calculator",
            "description": "Calculate the monthly investment required to reach a specified goal within a time horizon.",
            "href": "/tools/goal-calculator",
            "keywords": "goal investment calculator required monthly investment",
            "icon": "GOAL",
        },
        {
            "title": "Lumpsum Calculator",
            "description": "Estimate maturity value and estimated returns from a one-time investment.",
            "href": "/tools/lumpsum-calculator",
            "keywords": "lumpsum calculator maturity value expected returns",
            "icon": "LUMP",
        },
        {
            "title": "Compound Interest Calculator",
            "description": "Estimate interest earned and maturity value with a compounding frequency.",
            "href": "/tools/compound-interest-calculator",
            "keywords": "compound interest calculator maturity value interest earned",
            "icon": "CI",
        },
        {
            "title": "Inflation Calculator",
            "description": "Estimate future value and purchasing power impact from inflation over time.",
            "href": "/tools/inflation-calculator",
            "keywords": "inflation calculator future value purchasing power impact",
            "icon": "INF",
        },
        {
            "title": "Emergency Fund Calculator",
            "description": "Recommend emergency fund based on monthly expenses and coverage months.",
            "href": "/tools/emergency-fund-calculator",
            "keywords": "emergency fund calculator recommended emergency fund",
            "icon": "EF",
        },
        {
            "title": "Net Worth Calculator",
            "description": "Estimate net worth from total assets minus total liabilities.",
            "href": "/tools/net-worth-calculator",
            "keywords": "net worth calculator assets liabilities",
            "icon": "NW",
        },
    ]


    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "FinCalX India | SIP, EMI, Salary & Portfolio Calculators",
            "description": "Free SIP, EMI, salary, and portfolio overlap calculators for India. Fast, private, and no login required.",
            "tools": tools,
        },
    )


@router.api_route("/about", response_class=HTMLResponse, name="about_page", methods=["GET", "HEAD"])
async def about(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "title": "About FinCalX | Private Financial Calculators India",
            "description": "Learn about FinCalX, a privacy-friendly finance education platform with free SIP, EMI, salary, and portfolio overlap calculators.",
        },
    )
