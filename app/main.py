from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError


from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from pathlib import Path
import sys

from app.routers import contact, education, emi, home, legal, overlap, salary, sip, cagr
from app.routers import lumpsum, compound_interest, inflation, emergency_fund, net_worth, step_up_sip, swp, goal, retirement, fire
from app.routers import evergreen_calculators
from app.routers import tools_page
from app.services.evergreen_calculator_service import EVERGREEN_CALCULATORS



from app.security import RateLimitMiddleware, add_security_headers



# ============================
# ✅ LOGGING
# ============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("fincalx")

ALLOWED_ORIGINS = ["http://localhost:8000"]
CANONICAL_HOST = "getfincalx.com"
REDIRECT_HOSTS = {"www.getfincalx.com"}
ADS_TXT_PATH = Path("app/static/ads.txt")

# ============================
# ✅ MAIN APP (ONLY ONE!)
# ============================

app = FastAPI(
    title="FinCalX",
    description="Stateless calculators for SIP, EMI, Indian income tax, and portfolio overlap.",
    version="1.0.0",
    debug=False,
    docs_url=None,
    redoc_url=None,
)

# ============================
# ✅ SECURITY HEADERS
# ============================

app.middleware("http")(add_security_headers)


@app.middleware("http")
async def canonical_host_redirect(request: Request, call_next):
    if request.url.hostname in REDIRECT_HOSTS:
        url = request.url.replace(netloc=CANONICAL_HOST)
        return RedirectResponse(str(url), status_code=301)

    return await call_next(request)

# ============================
# ✅ TEMPLATES
# ============================

templates = Jinja2Templates(directory="app/templates")

# ============================
# ✅ SITEMAP (FIXED)
# ============================

@app.api_route("/sitemap.xml", methods=["GET", "HEAD"], include_in_schema=False)
async def sitemap():

    paths = [
        "/",
        "/tools",
        "/tools/sip-calculator",
        "/tools/emi-calculator",
        "/tools/salary-calculator",
        "/tools/portfolio-overlap-checker",
        "/tools/cagr-calculator",
        "/tools/step-up-sip-calculator",
        "/tools/swp-calculator",
        "/tools/goal-calculator",
        "/tools/retirement-calculator",
        "/tools/fire-calculator",
        "/tools/lumpsum-calculator",
        "/tools/compound-interest-calculator",
        "/tools/inflation-calculator",
        "/tools/emergency-fund-calculator",
        "/tools/net-worth-calculator",
        "/learning-center",
        "/finance-glossary",
        "/comparison-guides",
        "/financial-planning-resources",
        "/planning-tools",
        "/about",
        "/contact",
        "/privacy-policy",
        "/terms-of-service",
        "/disclaimer",
    ]
    paths.extend(f"/learning-center/{guide['slug']}" for guide in education.GUIDES)
    paths.extend(f"/comparison-guides/{item[0]}" for item in education.COMPARISONS)
    paths.extend(calculator.path for calculator in EVERGREEN_CALCULATORS)
    xml_urls = "\n".join(f"  <url><loc>https://getfincalx.com{path}</loc></url>" for path in dict.fromkeys(paths))
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_urls}
</urlset>"""
    return Response(content=xml_content.strip(), media_type="application/xml")

# ============================
# ✅ ROBOTS.TXT
# ============================

@app.api_route("/robots.txt", methods=["GET", "HEAD"], include_in_schema=False)
async def robots():

    return PlainTextResponse(
        content="User-agent: *\nAllow: /\nSitemap: https://getfincalx.com/sitemap.xml"
    )

# ============================
# ✅ ERROR HANDLERS
# ============================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"404: {request.url.path}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "title": "Page Not Found | FinCalX",
            "description": "Page not found.",
            "status_code": 404,
            "heading": "Page Not Found",
            "message": "The page you are looking for does not exist.",
        },
        status_code=404,
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error(f"500: {request.url.path} | error: {exc}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "title": "Server Error | FinCalX",
            "description": "Something went wrong.",
            "status_code": 500,
            "heading": "Something Went Wrong",
            "message": "Please try again later.",
        },
        status_code=500,
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc):
    logger.warning(f"422: {request.url.path}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "title": "Invalid Input | FinCalX",
            "description": "Invalid input.",
            "status_code": 422,
            "heading": "Invalid Input",
            "message": "Please check your inputs.",
        },
        status_code=422,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "title": "Server Error | FinCalX",
            "description": "Something went wrong.",
            "status_code": 500,
            "heading": "Something Went Wrong",
            "message": "Please try again later.",
        },
        status_code=500,
    )

# ============================
# ✅ MIDDLEWARES
# ============================

app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)







# ============================
# ✅ STATIC FILES
# ============================

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ============================
# ✅ ADS.TXT for AdSense
# ============================

@app.api_route("/ads.txt", methods=["GET", "HEAD"], include_in_schema=False)
async def ads_txt():

    return PlainTextResponse(
        ADS_TXT_PATH.read_text(encoding="utf-8").rstrip("\r\n"),
        media_type="text/plain",
    )
# ============================
# ✅ ROUTERS (Structured for Scalability)
# ============================

app.include_router(home.router)
app.include_router(contact.router)
app.include_router(education.router)
app.include_router(sip.router)
app.include_router(cagr.router)

app.include_router(lumpsum.router)
app.include_router(compound_interest.router)
app.include_router(inflation.router)
app.include_router(emergency_fund.router)
app.include_router(net_worth.router)
app.include_router(step_up_sip.router)
app.include_router(swp.router)
app.include_router(goal.router)
app.include_router(retirement.router)
app.include_router(fire.router)
app.include_router(evergreen_calculators.router)


app.include_router(emi.router)

app.include_router(salary.router)
app.include_router(tools_page.router)
# app.include_router(tax.router)  # Disabled
app.include_router(overlap.router)
app.include_router(legal.router)




# ============================================
# ✅ API ROUTES (Ready for AJAX/Future Apps)
# ============================================

# Legacy: API structure available in calculator_base.py
# Example API patterns:
# @app.get("/api/v1/emi")       # JSON API for EMI
# @app.get("/api/v1/sip")       # JSON API for SIP
# @app.post("/api/v1/calculate") # Universal calculate endpoint

