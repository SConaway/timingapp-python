# timingapp-python

Python client for the [Timing](https://timingapp.com) macOS app SQLite database.

Provides read-only access to Timing's SQLite database (`~/Library/Application Support/info.eurocomp.Timing2/SQLite.db`) via SQLAlchemy 2.x ORM.

> **Credit:** This is a Python port of [timingapp-ruby](https://github.com/marcoroth/timingapp-ruby) by [@marcoroth](https://github.com/marcoroth). The Ruby gem provides the same read-only database access via ActiveRecord; this library reimplements it idiomatically in Python using SQLAlchemy 2.x.

## Requirements

- Python 3.12+
- SQLAlchemy 2.0+
- macOS with Timing app installed (for real usage)

## Installation

```bash
pip install timingapp
```

## Usage

```python
from timingapp import open_database, AppActivity, Project, TaskActivity
from sqlalchemy import select

# Open the default Timing database (read-only)
db = open_database()

with db.session() as sess:
    # Query all projects
    projects = sess.scalars(select(Project)).all()
    for p in projects:
        print(p.title)

    # Get archived projects
    archived = sess.scalars(Project.archived()).all()

    # Get running task activities
    running = sess.scalars(TaskActivity.running()).all()

    # Get deleted app activities
    deleted = sess.scalars(AppActivity.deleted()).all()

    # Access relationships
    activity = sess.get(AppActivity, 1)
    if activity:
        print(activity.application.name)
        print(activity.project.title)
        print(activity.startDate)  # UTC datetime
```

## Models

| Model | Table | Notes |
|-------|-------|-------|
| `AppActivity` | `AppActivity` | Scopes: `deleted()` |
| `AppActivityWithStrings` | `AppActivityWithStrings` | SQLite VIEW |
| `Application` | `Application` | |
| `Device` | `Device` | PK: `localID` |
| `Event` | `Event` | |
| `EventSource` | `EventSource` | Scopes: `templates()`, `favorites()` |
| `EventSourceTaskActivity` | `EventSourceTaskActivity` | Scopes: `deleted()` |
| `Filter` | `Filter` | Scopes: `samples()`, self-referential |
| `Integration` | `Integration` | |
| `IntegrationLogResult` | `integration_log_result` | |
| `IntegrationProject` | `IntegrationProject` | |
| `Path` | `Path` | |
| `Project` | `Project` | Scopes: `archived()`, self-referential |
| `TaskActivity` | `TaskActivity` | Scopes: `running()`, `deleted()` |
| `Title` | `Title` | |

## Development

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Type check
uv run mypy src/
```
