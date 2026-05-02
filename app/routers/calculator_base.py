"""
Base Calculator Module

Provides a unified structure for all calculators with:
- Standard GET/POST endpoints
- AJAX/JSON API support ready
- Common form validation
- Shared context building
"""

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.forms import validate_form_data
from app.services.formatting import money, percent


class CalculatorBase(ABC):
    """Base class for all calculators."""

    # Class attributes to override in subclasses
    name: ClassVar[str]
    route: ClassVar[str]
    template: ClassVar[str]
    title: ClassVar[str]
    description: ClassVar[str]
    form_model: ClassVar[type]
    calculate_fn: ClassVar[callable]

    # Default form values
    defaults: ClassVar[dict] = {}

    def __init__(self):
        self.router = APIRouter(prefix="/tools", tags=["tools"])
        self._setup_routes()

    def _setup_routes(self):
        """Setup standard calculator routes."""
        self.router.add_api_route(
            self.route,
            self._get_page,
            methods=["GET"],
            name=f"{self.name}_page",
        )
        self.router.add_api_route(
            self.route,
            self._calculate,
            methods=["POST"],
            name=f"{self.name}_calculate",
        )

    async def _get_page(self, request: Request) -> HTMLResponse:
        """Render calculator page."""
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="app/templates")
        return templates.TemplateResponse(
            self.template,
            self._context(request),
        )

    async def _calculate(self, request: Request) -> HTMLResponse:
        """Process calculator form submission."""
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="app/templates")

        raw_form = dict(await request.form())
        data, errors, error = validate_form_data(self.form_model, raw_form)

        context = self._context(request, form=raw_form if errors else data.model_dump() if data else None)

        if errors:
            context["errors"] = errors
            context["error"] = error
            return templates.TemplateResponse(self.template, context)

        # Calculate result
        result = self._calculate_result(data)
        context["result"] = self._format_result(result)
        return templates.TemplateResponse(self.template, context)

    def _context(self, request: Request, form: dict | None = None) -> dict:
        """Build standard context for templates."""
        return {
            "request": request,
            "title": self.title,
            "description": self.description,
            "form": form or self.defaults.copy(),
        }

    @abstractmethod
    def _calculate_result(self, data: Any) -> dict:
        """Calculate result. Must be implemented by subclass."""
        pass

    def _format_result(self, result: dict) -> dict:
        """Format result values for display. Can be overridden."""
        return {key: money(value) for key, value in result.items()}


# ============================================
# LEGACY COMPATIBILITY FUNCTIONS
# ============================================

def create_context(
    request: Request,
    title: str,
    description: str,
    form: dict | None = None,
    defaults: dict | None = None,
) -> dict:
    """Create standard calculator context. Legacy compatibility."""
    return {
        "request": request,
        "title": title,
        "description": description,
        "form": form or defaults or {},
    }


def render_template(
    request: Request,
    template: str,
    context: dict,
) -> HTMLResponse:
    """Render template with context. Legacy compatibility."""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse(template, context)


def handle_form(
    request: Request,
    form_model: type,
    calculate_fn: callable,
    template: str,
    form_defaults: dict,
    title: str,
    description: str,
    format_result: bool = True,
) -> HTMLResponse:
    """
    Standard form handler for calculator routes.
    
    Args:
        request: FastAPI request
        form_model: Pydantic form model
        calculate_fn: Calculation function
        template: Template path
        form_defaults: Default form values
        title: Page title
        description: Page description
        format_result: Whether to format monetary values
    
    Returns:
        HTMLResponse with result
    """
    raw_form = dict(await request.form())
    data, errors, error = validate_form_data(form_model, raw_form)

    context = create_context(
        request,
        title,
        description,
        form=raw_form if errors else data.model_dump() if data else None,
        defaults=form_defaults,
    )

    if errors:
        context["errors"] = errors
        context["error"] = error
        return render_template(request, template, context)

    result = calculate_fn(**data.model_dump())
    
    if format_result:
        context["result"] = {key: money(value) for key, value in result.items()}
    else:
        context["result"] = result
    
    context["result_raw"] = result
    return render_template(request, template, context)
