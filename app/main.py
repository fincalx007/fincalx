from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import sys

from app.routers import emi, home, legal, overlap, sip
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

# ============================
# ✅ TEMPLATES
# ============================

templates = Jinja2Templates(directory="app/templates")

# ============================
# ✅ SITEMAP (FIXED)
# ============================

from fastapi.responses import Response

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    xml_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>https://getfincalx.com/</loc></url>\n'
        '  <url><loc>https://getfincalx.com/tools/sip-calculator</loc></url>\n'
        '  <url><loc>https://getfincalx.com/tools/emi-calculator</loc></url>\n'
        '  <url><loc>https://getfincalx.com/tools/portfolio-overlap-checker</loc></url>\n'
        '</urlset>'
    )

    response = Response(content=xml_content, media_type="application/xml")

    # 🚨 CRITICAL FIX: remove headers that break XML
    response.headers.pop("content-security-policy", None)

    return response
# ============================
# ✅ ROBOTS.TXT
# ============================

@app.get("/robots.txt", include_in_schema=False)
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
# ✅ ROUTERS
# ============================

app.include_router(home.router)
app.include_router(sip.router)
app.include_router(emi.router)
# app.include_router(tax.router)  # Disabled
app.include_router(overlap.router)
app.include_router(legal.router)
