from datetime import date

from sqlalchemy.orm import Session

from app import defaults
from app.models import PlanSettings, User


def get_or_create(db: Session, user: User) -> PlanSettings:
    current = db.get(PlanSettings, user.id)
    if current is not None:
        return current

    start, end = defaults.default_plan_window(date.today())
    current = PlanSettings(
        user_id=user.id,
        plan_start=start,
        plan_end=end,
        days_soon=defaults.DAYS_SOON,
        tight_limit=defaults.TIGHT_LIMIT,
        scenarios=list(defaults.SCENARIOS),
        product_categories=list(defaults.PRODUCT_CATEGORIES),
        income_categories=list(defaults.INCOME_CATEGORIES),
        expense_categories=list(defaults.EXPENSE_CATEGORIES),
    )
    db.add(current)
    db.commit()
    db.refresh(current)
    return current
