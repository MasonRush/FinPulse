from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, dashboard, transactions, investments, accounts
from app.middleware import SecurityHeadersMiddleware, RateLimitMiddleware
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinPulse API",
    description="Financial Health Dashboard API",
    version="1.0.0"
)

# OWASP: Security headers middleware (add first to apply to all responses)
app.add_middleware(SecurityHeadersMiddleware)

# OWASP: Rate limiting middleware (protect against brute force)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Configure CORS - OWASP: Restrictive CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],  # OWASP: Explicit methods only
    allow_headers=["Authorization", "Content-Type"],  # OWASP: Explicit headers only
    expose_headers=[],
    max_age=600,  # Cache preflight for 10 minutes
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(investments.router, prefix="/api/investments", tags=["investments"])

@app.get("/")
async def root():
    return {"message": "FinPulse API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

