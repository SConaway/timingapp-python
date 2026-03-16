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

    c.executescript("""
        CREATE TABLE Device (
            localID INTEGER PRIMARY KEY NOT NULL,
            globalID INTEGER NOT NULL,
            macAddress BLOB,
            displayName TEXT,
            property_bag TEXT
        );

        CREATE TABLE Application (
            id INTEGER PRIMARY KEY NOT NULL,
            bundleIdentifier TEXT,
            executable TEXT,
            title TEXT,
            property_bag TEXT
        );

        CREATE TABLE Title (
            id INTEGER PRIMARY KEY,
            stringValue TEXT
        );

        CREATE TABLE Path (
            id INTEGER PRIMARY KEY,
            stringValue TEXT
        );

        CREATE TABLE Project (
            id INTEGER PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            parentID INTEGER,
            listPosition INTEGER NOT NULL DEFAULT 0,
            isSample BOOLEAN NOT NULL DEFAULT 0,
            color TEXT NOT NULL DEFAULT '#000000',
            productivityScore REAL NOT NULL DEFAULT 0,
            predicate BLOB,
            ruleListPosition INTEGER NOT NULL DEFAULT 0,
            isArchived BOOLEAN NOT NULL DEFAULT 0,
            membershipID INTEGER,
            property_bag TEXT
        );

        CREATE TABLE AppActivity (
            id INTEGER PRIMARY KEY NOT NULL,
            localDeviceID INTEGER NOT NULL,
            startDate REAL NOT NULL,
            endDate REAL NOT NULL,
            applicationID INTEGER NOT NULL,
            titleID INTEGER,
            pathID INTEGER,
            projectID INTEGER,
            isDeleted BOOLEAN NOT NULL DEFAULT 0
        );

        CREATE TABLE TaskActivity (
            id INTEGER PRIMARY KEY NOT NULL,
            startDate REAL NOT NULL,
            endDate REAL NOT NULL,
            projectID INTEGER,
            title TEXT,
            notes TEXT,
            isDeleted BOOLEAN NOT NULL DEFAULT 0,
            isRunning BOOLEAN NOT NULL DEFAULT 0,
            property_bag TEXT
        );

        CREATE TABLE Integration (
            id INTEGER PRIMARY KEY,
            origin_id TEXT NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            icon BLOB,
            enabled_at REAL,
            last_updated_at REAL,
            paused_at REAL,
            deleted_at REAL,
            last_modified_origin REAL,
            last_modified_timing REAL,
            version INTEGER NOT NULL DEFAULT 1,
            api_status TEXT,
            event_visibility TEXT NOT NULL DEFAULT 'all',
            property_bag TEXT
        );

        CREATE TABLE IntegrationProject (
            id INTEGER PRIMARY KEY,
            integration_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            origin_id TEXT,
            timing_project_id INTEGER,
            last_modified_origin REAL,
            last_modified_timing REAL,
            deleted_by_integration_at REAL,
            hidden_at REAL,
            property_bag TEXT
        );

        CREATE TABLE EventSource (
            id INTEGER PRIMARY KEY,
            integration_id INTEGER NOT NULL,
            integration_project_id INTEGER,
            template_id INTEGER,
            is_template BOOL NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            notes TEXT,
            event_source_type TEXT NOT NULL DEFAULT 'calendar',
            origin_id TEXT,
            is_favorite BOOL NOT NULL DEFAULT 0,
            last_modified_origin REAL,
            last_modified_timing REAL,
            created_by_integration_at REAL,
            deleted_by_integration_at REAL,
            hidden_at REAL,
            property_bag TEXT
        );

        CREATE TABLE Event (
            id INTEGER PRIMARY KEY,
            integration_id INTEGER NOT NULL,
            event_source_id INTEGER NOT NULL,
            start_date REAL NOT NULL,
            end_date REAL,
            origin_id TEXT,
            event_action TEXT NOT NULL DEFAULT 'create',
            last_modified_origin REAL,
            last_modified_timing REAL,
            deleted_at REAL,
            property_bag TEXT
        );

        CREATE TABLE EventSourceTaskActivity (
            id INTEGER PRIMARY KEY,
            integration_id INTEGER NOT NULL,
            event_source_id INTEGER NOT NULL,
            task_activity_id INTEGER NOT NULL,
            deleted_at REAL,
            property_bag TEXT,
            event_id INTEGER DEFAULT NULL
        );

        CREATE TABLE integration_log_result (
            id INTEGER PRIMARY KEY,
            integration_id INTEGER NOT NULL,
            result INTEGER NOT NULL,
            error_message TEXT,
            timestamp REAL
        );

        CREATE TABLE Filter (
            id INTEGER PRIMARY KEY NOT NULL,
            parentID INTEGER,
            listPosition INTEGER NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            predicate BLOB,
            isSample BOOLEAN NOT NULL DEFAULT 0,
            property_bag TEXT
        );

        CREATE VIEW AppActivityWithStrings AS
        SELECT
            aa.id,
            aa.localDeviceID,
            aa.startDate,
            aa.endDate,
            aa.applicationID,
            aa.titleID,
            aa.pathID,
            t.stringValue,
            p.stringValue,
            aa.projectID
        FROM AppActivity aa
        LEFT JOIN Title t ON t.id = aa.titleID
        LEFT JOIN Path p ON p.id = aa.pathID
        WHERE aa.isDeleted = 0;
    """)

    c.executescript("""
        INSERT INTO Device VALUES (1, 100, NULL, 'MacBook Pro', NULL);
        INSERT INTO Device VALUES (2, 200, NULL, 'iPhone', NULL);

        INSERT INTO Application VALUES (1, 'com.apple.Safari', 'Safari', 'Safari', NULL);
        INSERT INTO Application VALUES (2, 'com.microsoft.VSCode', 'VSCode', 'VSCode', NULL);

        INSERT INTO Title VALUES (1, 'Google - Safari');
        INSERT INTO Title VALUES (2, 'main.py - VSCode');

        INSERT INTO Path VALUES (1, '/Applications/Safari.app');
        INSERT INTO Path VALUES (2, '/Applications/VSCode.app');

        INSERT INTO Project VALUES (1, 'Root Project', NULL, 0, 0, '#FF0000', 0, NULL, 0, 0, NULL, '{"key": "value"}');
        INSERT INTO Project VALUES (2, 'Child Project', 1, 1, 0, '#00FF00', 0, NULL, 0, 0, NULL, NULL);
        INSERT INTO Project VALUES (3, 'Archived Project', NULL, 2, 0, '#0000FF', 0, NULL, 0, 1, NULL, NULL);

        INSERT INTO AppActivity VALUES (1, 1, 1700000000.0, 1700003600.0, 1, 1, 1, 1, 0);
        INSERT INTO AppActivity VALUES (2, 1, 1700000000.0, 1700003600.0, 2, 2, 2, 2, 1);

        INSERT INTO TaskActivity VALUES (1, 1700000000.0, 1700003600.0, 1, 'Feature work', 'Working on feature', 0, 1, '{"tag": "dev"}');
        INSERT INTO TaskActivity VALUES (2, 1700000000.0, 1700003600.0, 2, 'Finished task', NULL, 0, 0, NULL);
        INSERT INTO TaskActivity VALUES (3, 1700000000.0, 1700003600.0, 1, 'Deleted task', NULL, 1, 0, NULL);

        INSERT INTO Integration VALUES (1, 'jira-origin', 'jira', 'Jira', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 'all', NULL);

        INSERT INTO IntegrationProject VALUES (1, 1, 'My Project', 'PROJ', 1, NULL, NULL, NULL, NULL, NULL);

        INSERT INTO EventSource VALUES (1, 1, NULL, NULL, 1, 'Template Source', NULL, 'calendar', NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL);
        INSERT INTO EventSource VALUES (2, 1, 1, 1, 0, 'Favorite Source', NULL, 'calendar', NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL);
        INSERT INTO EventSource VALUES (3, 1, NULL, NULL, 0, 'Regular Source', NULL, 'calendar', NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL);

        INSERT INTO Event VALUES (1, 1, 2, 1700000000.0, 1700003600.0, NULL, 'create', NULL, NULL, NULL, '{"extra": "data"}');

        INSERT INTO EventSourceTaskActivity VALUES (1, 1, 2, 1, NULL, NULL, NULL);
        INSERT INTO EventSourceTaskActivity VALUES (2, 1, 3, 2, 1700010000.0, NULL, 1);

        INSERT INTO integration_log_result VALUES (1, 1, 0, NULL, 1700000000.0);

        INSERT INTO Filter VALUES (1, NULL, 0, 'Root Filter', NULL, 0, NULL);
        INSERT INTO Filter VALUES (2, NULL, 1, 'Sample Filter', NULL, 1, NULL);
        INSERT INTO Filter VALUES (3, 1, 0, 'Child Filter', NULL, 0, NULL);
    """)

    conn.commit()
    conn.close()
    return p


@pytest.fixture(scope="session")
def db(synthetic_db: Path):
    """Return an opened Database backed by the synthetic test DB."""
    from timingapp._database import Database
    database = Database(synthetic_db)
    yield database
    database.close()
