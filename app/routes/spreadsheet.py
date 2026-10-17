from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import ImportReport
from app.services.spreadsheet_export import export_workbook
from app.services.spreadsheet_import import SpreadsheetError, import_workbook

router = APIRouter()

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
XLSX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.post("/import", response_model=ImportReport)
async def import_spreadsheet(
    file: UploadFile = File(...),
    dry_run: bool = Query(True, description="Só valida, sem gravar"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ImportReport:
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Arquivo maior que 5 MB")
    try:
        return import_workbook(db, user, content, dry_run=dry_run)
    except SpreadsheetError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc


@router.get("/export")
def export_spreadsheet(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Response:
    filename = f"entrix_{date.today():%Y-%m-%d}.xlsx"
    return Response(
        content=export_workbook(db, user),
        media_type=XLSX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
