from fastapi.responses import StreamingResponse
import io
import csv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database
from fastapi import Request
from pydantic import BaseModel
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import aliased
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/report", response_model=schemas.ReportResponse)
def submit_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    db_report = models.SystemReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports", response_model=List[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(models.SystemReport).order_by(models.SystemReport.timestamp.desc()).all()


class Report(BaseModel):
    machine_id: str
    os: str
    disk_encryption: bool
    os_updates: bool
    antivirus: bool
    sleep_settings: bool


@app.post("/report")
def receive_report(report: Report):
    machine_data[report.machine_id] = {
        "timestamp": datetime.utcnow().isoformat(),
        "os": report.os,
        "results": {
            "disk_encryption": report.disk_encryption,
            "os_updates": report.os_updates,
            "antivirus": report.antivirus,
            "sleep_settings": report.sleep_settings
        }
    }
    return {"message": "Report received"}

@app.get("/machines", response_model=List[schemas.ReportResponse])
def get_machines(
    os: str = Query(None, description="Filter by operating system"),
    disk_encryption: bool = Query(None, description="Filter by disk encryption status"),
    os_updates: bool = Query(None, description="Filter by OS updates status"),
    antivirus: bool = Query(None, description="Filter by antivirus status"),
    sleep_settings: bool = Query(None, description="Filter by sleep settings status"),
    db: Session = Depends(get_db),
):
    query = db.query(models.SystemReport)
    
    if os:
        query = query.filter(models.SystemReport.os == os)
    if disk_encryption is not None:
        query = query.filter(models.SystemReport.disk_encryption == disk_encryption)
    if os_updates is not None:
        query = query.filter(models.SystemReport.os_updates == os_updates)
    if antivirus is not None:
        query = query.filter(models.SystemReport.antivirus == antivirus)
    if sleep_settings is not None:
        query = query.filter(models.SystemReport.sleep_settings == sleep_settings)
    
    # To get latest status per machine, you can group by machine_id and get max timestamp.
    # But SQLAlchemy does not support group by + max easily; so for simplicity, let's get all reports filtered and then get latest per machine in Python.
    
    reports = query.order_by(models.SystemReport.machine_id, models.SystemReport.timestamp.desc()).all()
    
    latest_reports = {}
    for report in reports:
        if report.machine_id not in latest_reports:
            latest_reports[report.machine_id] = report
    
    return list(latest_reports.values())

@app.get("/machines/export")
def export_machines_csv(
    os: str = Query(None, description="Filter by operating system"),
    disk_encryption: bool = Query(None, description="Filter by disk encryption status"),
    os_updates: bool = Query(None, description="Filter by OS updates status"),
    antivirus: bool = Query(None, description="Filter by antivirus status"),
    sleep_settings: bool = Query(None, description="Filter by sleep settings status"),
    db: Session = Depends(get_db),
):
    query = db.query(models.SystemReport)
    
    if os:
        query = query.filter(models.SystemReport.os == os)
    if disk_encryption is not None:
        query = query.filter(models.SystemReport.disk_encryption == disk_encryption)
    if os_updates is not None:
        query = query.filter(models.SystemReport.os_updates == os_updates)
    if antivirus is not None:
        query = query.filter(models.SystemReport.antivirus == antivirus)
    if sleep_settings is not None:
        query = query.filter(models.SystemReport.sleep_settings == sleep_settings)
    
    reports = query.order_by(models.SystemReport.machine_id, models.SystemReport.timestamp.desc()).all()
    
    # Get latest report per machine
    latest_reports = {}
    for report in reports:
        if report.machine_id not in latest_reports:
            latest_reports[report.machine_id] = report
    
    # Prepare CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write CSV header
    writer.writerow([
        "machine_id", "os", "disk_encryption", "os_updates",
        "antivirus", "sleep_settings", "timestamp"
    ])
    
    # Write rows
    for report in latest_reports.values():
        writer.writerow([
            report.machine_id,
            report.os,
            report.disk_encryption,
            report.os_updates,
            report.antivirus,
            report.sleep_settings,
            report.timestamp.isoformat()
        ])
    
    output.seek(0)
    
    # Return as streaming response with CSV mime type and attachment
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=machines_report.csv"}
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)