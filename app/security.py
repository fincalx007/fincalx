import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware


async def add_security_headers(request: Request, call_next: Callable) -> Response:
    """Add security headers to every response.

    Designed for use with @app.middleware("http") decorator.
    Only modifies response headers — never touches response.body.
    """
    response: Response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )
    return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter.

    IMPORTANT: This middleware only inspects the request and either:
      - returns a new PlainTextResponse (429), or
      - passes the request through with call_next(request).
    It does NOT read, write, or modify response.body.
    """

    def __init__(self, app, max_requests: int = 80, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_host = request.client.host if request.client else "unknown"
        now = time.monotonic()
        timestamps = self.requests[client_host]

        # Evict stale entries
        while timestamps and now - timestamps[0] > self.window_seconds:
            timestamps.popleft()

        if len(timestamps) >= self.max_requests:
            return PlainTextResponse(
                "Too many requests. Please try again later.",
                status_code=429,
            )

        timestamps.append(now)

        # Pass through without modifying the response body
        return await call_next(request)

