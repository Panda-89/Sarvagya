from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class SystemReport(Base):
    __tablename__ = "system_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    os = Column(String)
    disk_encryption = Column(Boolean)
    os_updates = Column(Boolean)
    antivirus = Column(Boolean)
    sleep_settings = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)