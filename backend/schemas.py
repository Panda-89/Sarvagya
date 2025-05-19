from pydantic import BaseModel
from datetime import datetime

class ReportCreate(BaseModel):
    machine_id: str
    os: str
    disk_encryption: bool
    os_updates: bool
    antivirus: bool
    sleep_settings: bool

class ReportResponse(ReportCreate):
    timestamp: datetime