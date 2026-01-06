"""
Security middleware for OWASP best practices
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    OWASP: Add security headers to all responses
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # OWASP: Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # OWASP: Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # OWASP: Enable XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # OWASP: Strict Transport Security (HTTPS only)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # OWASP: Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'"
        )
        
        # OWASP: Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # OWASP: Permissions Policy
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware (OWASP: Prevent brute force attacks)
    For production, use a proper rate limiting library like slowapi
    """
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        # OWASP: Rate limiting on authentication endpoints
        if "/api/auth/" in str(request.url):
            client_ip = request.client.host if request.client else "unknown"
            current_time = time.time()
            
            # Clean old entries
            self.requests = {
                ip: timestamps for ip, timestamps in self.requests.items()
                if current_time - max(timestamps) < 60
            }
            
            # Check rate limit
            if client_ip in self.requests:
                recent_requests = [
                    ts for ts in self.requests[client_ip]
                    if current_time - ts < 60
                ]
                if len(recent_requests) >= self.requests_per_minute:
                    from fastapi import HTTPException, status
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Too many requests. Please try again later."
                    )
                self.requests[client_ip].append(current_time)
            else:
                self.requests[client_ip] = [current_time]
        
        response = await call_next(request)
        return response

