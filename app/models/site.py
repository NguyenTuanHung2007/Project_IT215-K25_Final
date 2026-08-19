from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class ConstructionSite(Base):
    __tablename__ = 'construction_sites'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="construction_sites")
    site_memberships = relationship("SiteMember", back_populates="site")
    work_items = relationship("WorkItem", back_populates="site")
    
class SiteMember(Base):
    __tablename__ = 'site_members'

    site_id = Column(Integer, ForeignKey('construction_sites.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role = Column(String(50), nullable=False)
    joined_at = Column(DateTime, nullable=False)

    site = relationship("ConstructionSite", back_populates="site_memberships")
    user = relationship("User", back_populates="site_memberships")
    