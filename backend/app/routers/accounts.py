from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Account
from app.schemas import AccountCreate, AccountResponse, AccountUpdate
from app.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[AccountResponse])
def get_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    return [AccountResponse.model_validate(acc) for acc in accounts]

@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = Account(
        user_id=current_user.id,
        **account.dict()
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return AccountResponse.model_validate(db_account)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse.model_validate(account)

@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update fields if provided
    if account_update.balance is not None:
        account.balance = account_update.balance
    if account_update.institution_name is not None:
        account.institution_name = account_update.institution_name
    
    db.commit()
    db.refresh(account)
    return AccountResponse.model_validate(account)

