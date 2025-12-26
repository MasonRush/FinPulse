from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from app.database import get_db
from app.models import User, Account, Transaction, TransactionCategory
from app.schemas import TransactionCreate, TransactionResponse
from app.security import get_current_user

router = APIRouter()

@router.post("/upload", response_model=List[TransactionResponse])
async def upload_transactions(
    file: UploadFile = File(...),
    account_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify account belongs to user
    if account_id:
        account = db.query(Account).filter(
            Account.id == account_id,
            Account.user_id == current_user.id
        ).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
    
    # Read CSV file
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    # Expected columns: amount, category, description, timestamp
    required_columns = ["amount", "category"]
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {', '.join(required_columns)}"
        )
    
    # If account_id not provided, use first account or create one
    if not account_id:
        account = db.query(Account).filter(Account.user_id == current_user.id).first()
        if not account:
            raise HTTPException(
                status_code=400,
                detail="No account found. Please create an account first or specify account_id"
            )
        account_id = account.id
    
    transactions = []
    for _, row in df.iterrows():
        # Parse category
        try:
            category = TransactionCategory(row.get("category", "other").lower())
        except ValueError:
            category = TransactionCategory.OTHER
        
        transaction = Transaction(
            account_id=account_id,
            amount=float(row["amount"]),
            category=category,
            description=row.get("description"),
            timestamp=pd.to_datetime(row.get("timestamp")) if "timestamp" in row else None
        )
        db.add(transaction)
        transactions.append(transaction)
    
    db.commit()
    
    return [TransactionResponse.model_validate(t) for t in transactions]

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).join(Account).filter(
        Account.user_id == current_user.id
    ).order_by(Transaction.timestamp.desc()).offset(skip).limit(limit).all()
    
    return [TransactionResponse.model_validate(t) for t in transactions]

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify account belongs to user
    account = db.query(Account).filter(
        Account.id == transaction.account_id,
        Account.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    
    # Update account balance
    account.balance += transaction.amount
    db.commit()
    db.refresh(db_transaction)
    
    return TransactionResponse.model_validate(db_transaction)

@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the transaction and verify it belongs to the user
    transaction = db.query(Transaction).join(Account).filter(
        Transaction.id == transaction_id,
        Account.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Get the account to update balance
    account = db.query(Account).filter(Account.id == transaction.account_id).first()
    
    # Reverse the transaction amount from account balance
    account.balance -= transaction.amount
    
    # Delete the transaction
    db.delete(transaction)
    db.commit()
    
    return None

