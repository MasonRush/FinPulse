from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import yfinance as yf
from app.database import get_db
from app.models import User, Portfolio
from app.schemas import InvestmentPerformance, PortfolioResponse, PortfolioCreate
from app.security import get_current_user

router = APIRouter()

def get_stock_price(ticker: str) -> float:
    """Fetch current stock price using Yahoo Finance API via yfinance."""
    try:
        stock = yf.Ticker(ticker)
        # Get the most recent price data
        info = stock.info
        # Try to get current price from info, fallback to fast_info or history
        if 'currentPrice' in info and info['currentPrice']:
            return float(info['currentPrice'])
        elif 'regularMarketPrice' in info and info['regularMarketPrice']:
            return float(info['regularMarketPrice'])
        else:
            # Fallback: get the latest close price from recent history
            hist = stock.history(period="1d")
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
            else:
                # If no data, try fast_info
                fast_info = stock.fast_info
                if hasattr(fast_info, 'lastPrice') and fast_info.lastPrice:
                    return float(fast_info.lastPrice)
                raise ValueError(f"No price data available for {ticker}")
    except Exception as e:
        # Return None to indicate failure, let caller handle it
        raise ValueError(f"Could not fetch price for ticker {ticker}: {str(e)}")

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio (simplified version)."""
    if not returns or len(returns) < 2:
        return 0.0
    
    import statistics
    mean_return = statistics.mean(returns)
    std_dev = statistics.stdev(returns) if len(returns) > 1 else 0.0
    
    if std_dev == 0:
        return 0.0
    
    return (mean_return - risk_free_rate) / std_dev

@router.get("/performance", response_model=InvestmentPerformance)
def get_investment_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    
    if not portfolios:
        return InvestmentPerformance(
            total_value=0.0,
            total_cost_basis=0.0,
            total_return=0.0,
            total_return_percentage=0.0,
            time_weighted_return=0.0,
            sharpe_ratio=None,
            asset_allocation=[]
        )
    
    total_value = 0.0
    total_cost_basis = 0.0
    asset_allocation = []
    
    for portfolio in portfolios:
        try:
            current_price = get_stock_price(portfolio.ticker_symbol)
            current_value = current_price * portfolio.shares_owned
        except (ValueError, Exception) as e:
            # If we can't get the price, use cost basis as fallback
            # This prevents one bad ticker from breaking the entire performance calculation
            current_value = portfolio.cost_basis * portfolio.shares_owned
            current_price = portfolio.cost_basis
        cost_basis = portfolio.cost_basis * portfolio.shares_owned
        
        total_value += current_value
        total_cost_basis += cost_basis
        
        asset_allocation.append({
            "ticker": portfolio.ticker_symbol,
            "value": current_value,
            "percentage": 0.0  # Will calculate after total_value is known
        })
    
    # Calculate percentages
    if total_value > 0:
        for asset in asset_allocation:
            asset["percentage"] = (asset["value"] / total_value) * 100
    
    total_return = total_value - total_cost_basis
    total_return_percentage = (total_return / total_cost_basis * 100) if total_cost_basis > 0 else 0.0
    
    # Simplified TWR calculation (in production, use proper time-weighted return formula)
    time_weighted_return = total_return_percentage / 100.0
    
    # Calculate Sharpe ratio (simplified - would need historical data in production)
    sharpe_ratio = None  # Would require historical return data
    
    return InvestmentPerformance(
        total_value=total_value,
        total_cost_basis=total_cost_basis,
        total_return=total_return,
        total_return_percentage=total_return_percentage,
        time_weighted_return=time_weighted_return,
        sharpe_ratio=sharpe_ratio,
        asset_allocation=asset_allocation
    )

@router.get("/", response_model=List[PortfolioResponse])
def get_portfolios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    return [PortfolioResponse.model_validate(p) for p in portfolios]

@router.post("/", response_model=PortfolioResponse, status_code=201)
def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_portfolio = Portfolio(
        user_id=current_user.id,
        **portfolio.dict()
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return PortfolioResponse.model_validate(db_portfolio)

@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    db.delete(portfolio)
    db.commit()
    return None

