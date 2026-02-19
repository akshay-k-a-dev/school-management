from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import services
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/admin/dashboard", tags=["admin"])


@router.get("/stats")
def stats(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    return services.dashboard_service.get_dashboard_stats(db)


@router.get("/recent")
def recent(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    return {"recent": services.dashboard_service.get_recent_activity(db)}


@router.get('/export')
def export_report(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Export events + complaints + bookings as a simple PDF report (admin only)."""
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admin only')

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except Exception:
        raise HTTPException(status_code=500, detail='PDF export requires the reportlab package (pip install reportlab)')

    from io import BytesIO
    from app import models

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elems = []
    elems.append(Paragraph('Campus Service Hub - Exported Report', styles['Title']))
    elems.append(Spacer(1, 12))

    # stats
    stats = services.dashboard_service.get_dashboard_stats(db)
    elems.append(Paragraph('Overview', styles['Heading2']))
    elems.append(Paragraph(f"Users: {stats['users']} — Events: {stats['events']} — Complaints: {stats['complaints']} — Bookings: {stats['bookings']}", styles['Normal']))
    elems.append(Spacer(1, 12))

    # events
    events = db.query(models.Event).order_by(models.Event.date.asc()).all()
    elems.append(Paragraph('Events', styles['Heading2']))
    if events:
        data = [['ID', 'Title', 'Date', 'Venue', 'Capacity']]
        for e in events:
            data.append([str(e.id), e.title or '', str(e.date), e.venue or '', str(e.capacity or '')])
        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightblue), ('GRID', (0,0), (-1,-1), 0.25, colors.grey)]))
        elems.append(t)
    else:
        elems.append(Paragraph('No events', styles['Normal']))
    elems.append(Spacer(1, 12))

    # complaints
    complaints = db.query(models.Complaint).order_by(models.Complaint.created_at.desc()).all()
    elems.append(Paragraph('Complaints', styles['Heading2']))
    if complaints:
        data = [['ID', 'User', 'Title', 'Category', 'Status', 'Created']]
        for c in complaints:
            data.append([str(c.id), str(c.user_id), (c.title or '')[:40], (c.category or ''), c.status or '', str(c.created_at)])
        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.lightgrey), ('GRID', (0,0), (-1,-1), 0.25, colors.grey)]))
        elems.append(t)
    else:
        elems.append(Paragraph('No complaints', styles['Normal']))
    elems.append(Spacer(1, 12))

    # bookings
    bookings = db.query(models.Booking).order_by(models.Booking.date.desc()).all()
    elems.append(Paragraph('Bookings', styles['Heading2']))
    if bookings:
        data = [['ID', 'User', 'Room', 'Date', 'Start', 'End', 'Status']]
        for b in bookings:
            data.append([str(b.id), str(b.user_id), b.room_name or '', str(b.date), str(b.start_time), str(b.end_time), b.status or ''])
        t = Table(data, hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.beige), ('GRID', (0,0), (-1,-1), 0.25, colors.grey)]))
        elems.append(t)
    else:
        elems.append(Paragraph('No bookings', styles['Normal']))

    doc.build(elems)
    buffer.seek(0)
    from fastapi.responses import StreamingResponse
    return StreamingResponse(buffer, media_type='application/pdf', headers={ 'Content-Disposition': 'attachment; filename="chattan_report.pdf"' })
