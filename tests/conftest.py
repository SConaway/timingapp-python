import platform
import sqlite3
from pathlib import Path

import pytest

from timingapp._database import DEFAULT_DB_PATH

REAL_DB = DEFAULT_DB_PATH

macos_only = pytest.mark.skipif(
    not (platform.system() == "Darwin" and REAL_DB.exists()),
    reason="requires macOS Timing database",
)


@pytest.fixture(scope="session")
def synthetic_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build temp SQLite with Timing schema + fake rows. No real data."""
    p = tmp_path_factory.mktemp("db") / "test.db"
    conn = sqlite3.connect(str(p))
    c = conn.cursor()

    # Create tables
    c.executescript("""
        CREATE TABLE IF NOT EXISTS Device (
            localID INTEGER PRIMARY KEY,
            name TEXT,
            uuid TEXT,
            local_device INTEGER
        );

        CREATE TABLE IF NOT EXISTS Application (
            id INTEGER PRIMARY KEY,
            bundleIdentifier TEXT,
            name TEXT,
            category TEXT,
            is_productivity_app INTEGER
        );

        CREATE TABLE IF NOT EXISTS Title (
            id INTEGER PRIMARY KEY,
            stringValue TEXT
        );

        CREATE TABLE IF NOT EXISTS Path (
            id INTEGER PRIMARY KEY,
            stringValue TEXT
        );

        CREATE TABLE IF NOT EXISTS Project (
            id INTEGER PRIMARY KEY,
            title TEXT,
            color TEXT,
            parentID INTEGER,
            is_archived INTEGER DEFAULT 0,
            property_bag TEXT
        );

        CREATE TABLE IF NOT EXISTS AppActivity (
            id INTEGER PRIMARY KEY,
            startDate REAL,
            endDate REAL,
            deviceID INTEGER,
            applicationID INTEGER,
            titleID INTEGER,
            pathID INTEGER,
            projectID INTEGER,
            deleted_at REAL
        );

        CREATE TABLE IF NOT EXISTS TaskActivity (
            id INTEGER PRIMARY KEY,
            startDate REAL,
            endDate REAL,
            projectID INTEGER,
            notes TEXT,
            property_bag TEXT,
            deleted_at REAL
        );

        CREATE TABLE IF NOT EXISTS Integration (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            configuration TEXT
        );

        CREATE TABLE IF NOT EXISTS IntegrationProject (
            id INTEGER PRIMARY KEY,
            integrationID INTEGER,
            projectID INTEGER,
            external_id TEXT
        );

        CREATE TABLE IF NOT EXISTS EventSource (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            is_template INTEGER DEFAULT 0,
            is_favorite INTEGER DEFAULT 0,
            templateID INTEGER
        );

        CREATE TABLE IF NOT EXISTS Event (
            id INTEGER PRIMARY KEY,
            startDate REAL,
            endDate REAL,
            title TEXT,
            notes TEXT,
            sourceID INTEGER,
            property_bag TEXT
        );

        CREATE TABLE IF NOT EXISTS EventSourceTaskActivity (
            id INTEGER PRIMARY KEY,
            eventSourceID INTEGER,
            taskActivityID INTEGER,
            deleted_at REAL
        );

        CREATE TABLE IF NOT EXISTS integration_log_result (
            id INTEGER PRIMARY KEY,
            integrationID INTEGER,
            timestamp REAL,
            result TEXT,
            details TEXT
        );

        CREATE TABLE IF NOT EXISTS Filter (
            id INTEGER PRIMARY KEY,
            name TEXT,
            parentID INTEGER,
            is_sample INTEGER DEFAULT 0,
            criteria TEXT
        );

        CREATE VIEW IF NOT EXISTS AppActivityWithStrings AS
        SELECT
            aa.id,
            aa.startDate,
            aa.endDate,
            app.bundleIdentifier,
            app.name AS app_name,
            t.stringValue,
            aa.projectID,
            p.title AS project_title,
            aa.deviceID
        FROM AppActivity aa
        LEFT JOIN Application app ON app.id = aa.applicationID
        LEFT JOIN Title t ON t.id = aa.titleID
        LEFT JOIN Project p ON p.id = aa.projectID;
    """)

    # Insert synthetic data
    c.executescript("""
        INSERT INTO Device VALUES (1, 'MacBook Pro', 'test-uuid-1', 1);
        INSERT INTO Device VALUES (2, 'iPhone', 'test-uuid-2', 0);

        INSERT INTO Application VALUES (1, 'com.apple.Safari', 'Safari', 'Browser', 0);
        INSERT INTO Application VALUES (2, 'com.microsoft.VSCode', 'VSCode', 'Developer Tools', 1);

        INSERT INTO Title VALUES (1, 'Google - Safari');
        INSERT INTO Title VALUES (2, 'main.py - VSCode');

        INSERT INTO Path VALUES (1, '/Applications/Safari.app');
        INSERT INTO Path VALUES (2, '/Applications/VSCode.app');

        INSERT INTO Project VALUES (1, 'Root Project', '#FF0000', NULL, 0, '{"key": "value"}');
        INSERT INTO Project VALUES (2, 'Child Project', '#00FF00', 1, 0, NULL);
        INSERT INTO Project VALUES (3, 'Archived Project', '#0000FF', NULL, 1, NULL);

        INSERT INTO AppActivity VALUES (1, 1700000000.0, 1700003600.0, 1, 1, 1, 1, 1, NULL);
        INSERT INTO AppActivity VALUES (2, 1700000000.0, 1700003600.0, 1, 2, 2, 2, 2, 1700010000.0);

        INSERT INTO TaskActivity VALUES (1, 1700000000.0, NULL, 1, 'Working on feature', '{"tag": "dev"}', NULL);
        INSERT INTO TaskActivity VALUES (2, 1700000000.0, 1700003600.0, 2, 'Finished task', NULL, NULL);
        INSERT INTO TaskActivity VALUES (3, 1700000000.0, 1700003600.0, 1, 'Deleted task', NULL, 1700010000.0);

        INSERT INTO Integration VALUES (1, 'Jira', 'jira', '{}');
        INSERT INTO IntegrationProject VALUES (1, 1, 1, 'PROJ-123');

        INSERT INTO EventSource VALUES (1, 'Template Source', 'calendar', 1, 0, NULL);
        INSERT INTO EventSource VALUES (2, 'Favorite Source', 'calendar', 0, 1, 1);
        INSERT INTO EventSource VALUES (3, 'Regular Source', 'calendar', 0, 0, NULL);

        INSERT INTO Event VALUES (1, 1700000000.0, 1700003600.0, 'Test Event', 'Notes here', 2, '{"extra": "data"}');

        INSERT INTO EventSourceTaskActivity VALUES (1, 2, 1, NULL);
        INSERT INTO EventSourceTaskActivity VALUES (2, 3, 2, 1700010000.0);

        INSERT INTO integration_log_result VALUES (1, 1, 1700000000.0, 'success', '{"items": 5}');

        INSERT INTO Filter VALUES (1, 'Root Filter', NULL, 0, '{"type": "all"}');
        INSERT INTO Filter VALUES (2, 'Sample Filter', NULL, 1, '{"type": "sample"}');
        INSERT INTO Filter VALUES (3, 'Child Filter', 1, 0, NULL);
    """)

    conn.commit()
    conn.close()
    return p


@pytest.fixture(scope="session")
def db(synthetic_db: Path):
    """Return an opened Database backed by the synthetic test DB."""
    from timingapp._database import Database
    return Database(synthetic_db)
