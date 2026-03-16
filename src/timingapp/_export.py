import json
import sys
from datetime import date, datetime, timezone

from sqlalchemy import select

from timingapp._database import DEFAULT_DB_PATH, Database
from timingapp.models.app_activity import AppActivity


def export(argv: list[str] | None = None) -> None:
    args = argv if argv is not None else sys.argv[1:]

    if args:
        try:
            target = date.fromisoformat(args[0])
        except ValueError:
            print("Usage: timing-export YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)
    else:
        target = date.today()

    start = datetime(target.year, target.month, target.day, 0, 0, 0, tzinfo=timezone.utc)
    end = datetime(target.year, target.month, target.day, 23, 59, 59, tzinfo=timezone.utc)

    db = Database(DEFAULT_DB_PATH)

    stmt = (
        select(AppActivity)
        .where(AppActivity.startDate >= start, AppActivity.startDate <= end)
        .order_by(AppActivity.startDate)
    )

    with db.session() as sess:
        for activity in sess.scalars(stmt):
            print(json.dumps({
                "startDate": activity.startDate.isoformat() if activity.startDate else None,
                "endDate": activity.endDate.isoformat() if activity.endDate else None,
                "appName": activity.application.title if activity.application else None,
                "windowTitle": activity.title.stringValue if activity.title else None,
                "path": activity.path.stringValue if activity.path else None,
                "device": activity.device.displayName if activity.device else None,
            }))
