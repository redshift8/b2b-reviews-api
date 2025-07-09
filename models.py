from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key = True, index = True)
    author_name = Column(String, index = True)
    rating = Column(Integer)
    comment= Column(String)
    created_at = Column(DateTime, default=func.now())
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", backref = "reviews")


class Company(Base):
    __tablename__="companies"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    description = Column(String)
