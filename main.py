from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Review, Company 
from schemas import ReviewCreate, ReviewRead, CompanyCreate, CompanyRead
from typing import List
from datetime import date
from sqlalchemy import desc, asc

app = FastAPI()

@app.post("/company", response_model = CompanyRead)
def create_company(company : CompanyCreate, db: Session = Depends(get_db)):
    new_company= Company(**company.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@app.get("/company", response_model = list[CompanyRead])
def get_companies(db : Session = Depends(get_db)):
    company = db.query(Company).all()
    return company

@app.get("/company/{company_id}", response_model = CompanyRead)
def get_company_id(company_id : int, db : Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.post("/reviews", response_model =ReviewRead )
def create_reviews(review : ReviewCreate, db : Session = Depends(get_db)):
    new_review = Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get("/reviews", response_model=List[ReviewRead])
def get_reviews(
    db: Session = Depends(get_db),
    company_id: int = Query(None),
    min_rating: int = Query(None, ge=1, le=5),
    start_date: date = Query(None),
    end_date: date = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    query = db.query(Review)

    if company_id is not None:
        query = query.filter(Review.company_id == company_id)
    if min_rating is not None:
        query = query.filter(Review.rating >= min_rating)
    if start_date:
        query = query.filter(Review.created_at >= start_date)
    if end_date:
        query = query.filter(Review.created_at <= end_date)

    sort_column = getattr(Review, sort_by, None)
    if sort_column is not None:
        query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    return query.all()

@app.get("/company/{company_id}/reviews", response_model=List[ReviewRead])
def get_reviews_for_company(
    company_id: int,
    db: Session = Depends(get_db),
    min_rating: int = Query(None, ge=1, le=5),
    start_date: date = Query(None),
    end_date: date = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    query = db.query(Review).filter(Review.company_id == company_id)

    if min_rating is not None:
        query = query.filter(Review.rating >= min_rating)
    if start_date:
        query = query.filter(Review.created_at >= start_date)
    if end_date:
        query = query.filter(Review.created_at <= end_date)

    sort_column = getattr(Review, sort_by, None)
    if sort_column is not None:
        query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    return query.all()


    