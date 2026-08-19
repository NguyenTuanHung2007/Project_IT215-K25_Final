from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from db.database import Base

class WorkItem(Base):
    __tablename__ = 'work_items'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('construction_sites.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)

    site = relationship("ConstructionSite", back_populates="work_items")
    assignee = relationship("User", back_populates="assigned_work_items")