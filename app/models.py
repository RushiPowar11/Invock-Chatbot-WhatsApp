from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Lead(Base):
	__tablename__ = "leads"

	id = Column(Integer, primary_key=True, index=True)
	phone = Column(String(32), unique=True, index=True, nullable=False)
	full_name = Column(String(255), nullable=True)
	email = Column(String(255), nullable=True)
	business_name = Column(String(255), nullable=True)
	stage = Column(String(64), nullable=False, default="start")  # start|ask_name|ask_email|ask_business|ready_to_schedule|scheduled
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
