from click import option
from flask.cli import AppGroup
import datetime
import logging
from redash.models.base import db
from redash.models import Dashboard, Event
from sqlalchemy import func, cast


logging.getLogger('xmlschema').setLevel(logging.WARNING)


manager = AppGroup(help="Show event infos")


@manager.command(name="per_dashboard", help="List event counts per dashboard from the last day")
@option('--json', is_flag=True, help='Output info in JSON format.')
def list_events(json):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    dashboard_event_counts = db.session.query(
        Dashboard.name,
        func.count()
    ).select_from(Event).join(
        Dashboard,
        Dashboard.id == cast(Event.object_id, db.Integer)
    ).filter(
        Event.object_type == 'dashboard',
        Event.created_at >= yesterday,
        Event.created_at < today
    ).group_by(
        Dashboard.name
    ).all()

    if json:
        print(dashboard_event_counts)
    else:
        for dashboard, count in dashboard_event_counts:
            print(f"{dashboard} {count}")
