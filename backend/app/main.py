from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, dashboard, transactions, investments, accounts

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinPulse API",
    description="Financial Health Dashboard API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

