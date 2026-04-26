from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from app.routers import emi, home, legal, overlap, sip, tax
from app.security import RateLimitMiddleware, SecurityHeadersMiddleware

ALLOWED_ORIGINS = ["http://localhost:8000"]

app = FastAPI(
    title="FinCalX",
    description="Stateless calculators for SIP, EMI, Indian income tax, and portfolio overlap.",
    version="1.0.0",
    debug=False,
    docs_url=None,
    redoc_url=None,
)

# ✅ CLEAN SITEMAP (FIXED)
@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://getfincalx.com/</loc></url>
    <url><loc>https://getfincalx.com/tools/sip-calculator</loc></url>
    <url><loc>https://getfincalx.com/tools/emi-calculator</loc></url>
    <url><loc>https://getfincalx.com/tools/income-tax-calculator</loc></url>
    <url><loc>https://getfincalx.com/tools/portfolio-overlap-checker</loc></url>
</urlset>
"""
    return Response(content=xml_content, media_type="application/xml")


# ✅ ROBOTS.TXT
@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return PlainTextResponse(
        content="User-agent: *\n"
                "Allow: /\n"
                "Sitemap: https://getfincalx.com/sitemap.xml"
    )


# ✅ MIDDLEWARES
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# ✅ STATIC FILES
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ ROUTERS
app.include_router(home.router)
app.include_router(sip.router)
app.include_router(emi.router)
app.include_router(tax.router)
app.include_router(overlap.router)
app.include_router(legal.router)