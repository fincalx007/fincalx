from __future__ import annotations

from typing import Any, Callable, Iterable, Optional

from fastapi.routing import APIRouter


def get_with_head(
    router: APIRouter,
    path: str,
    **kwargs: Any,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Register a route so it supports both GET and HEAD.

    Usage:
        @get_with_head(router, "/about", response_class=HTMLResponse)
        async def about(...):
            ...

    Implementation detail:
    - FastAPI/Starlette already implements correct HEAD semantics *when a route
      explicitly supports HEAD*. By using methods=["GET","HEAD"], we avoid
      405 Method Not Allowed for HEAD requests.
    """

    # FastAPI endpoints accept `methods` for api_route; for router.get we need router.api_route.
    methods = list(kwargs.pop("methods", None) or [])
    if "GET" not in methods:
        methods.append("GET")
    if "HEAD" not in methods:
        methods.append("HEAD")

    return router.api_route(path, methods=methods, **kwargs)

