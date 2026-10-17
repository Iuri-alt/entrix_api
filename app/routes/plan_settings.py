from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import PlanSettings, User
from app.schemas import PlanSettingsIn, PlanSettingsOut
from app.services import plan_settings

router = APIRouter()


@router.get("/", response_model=PlanSettingsOut)
def read_settings(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> PlanSettings:
    return plan_settings.get_or_create(db, user)


@router.put("/", response_model=PlanSettingsOut)
def update_settings(
    body: PlanSettingsIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PlanSettings:
    current = plan_settings.get_or_create(db, user)
    for field, value in body.model_dump().items():
        setattr(current, field, value)
    db.commit()
    db.refresh(current)
    return current
