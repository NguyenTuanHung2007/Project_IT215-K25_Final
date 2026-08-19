from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(String(20), default='USER')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)

    construction_sites = relationship("ConstructionSite", back_populates="owner")
    site_memberships = relationship("SiteMember", back_populates="user")
    assigned_work_items = relationship("WorkItem", back_populates="assignee")