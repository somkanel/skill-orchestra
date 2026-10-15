#!/usr/bin/env python3
"""Local, opt-in-by-recording usage ledger. Reading never creates a database."""

import argparse
from contextlib import closing
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
import sys

DEFAULT_DB = Path.home() / '.skill-orchestra' / 'usage.sqlite3'


def moment(now=None):
    value = now if now is not None else datetime.now(timezone.utc)
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('Timestamp must include a timezone')
    return value.astimezone(timezone.utc)


def canonical(skill):
    path = Path(skill).expanduser()
    if not path.is_absolute():
        raise ValueError('Skill path must be absolute')
    return str(path.resolve())


def record(skill, task_id, database=DEFAULT_DB, now=None):
    path = canonical(skill)
    if not Path(path).is_file() or Path(path).name != 'SKILL.md':
        raise ValueError('Recording requires an existing SKILL.md')
    if not isinstance(task_id, str) or not task_id.strip():
        raise ValueError('An opaque task ID is required')
    timestamp = moment(now).isoformat(timespec='microseconds')
    database = Path(database).expanduser()
    database.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(database, timeout=10)) as connection, connection:
        connection.execute('BEGIN IMMEDIATE')
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        if version not in (0, 1) or (version == 0 and tables):
            raise ValueError('Unsupported usage database; refusing to change it')
        connection.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        connection.execute('CREATE TABLE IF NOT EXISTS events (skill_path TEXT NOT NULL, task_id TEXT NOT NULL, '
                           'used_at TEXT NOT NULL, PRIMARY KEY (skill_path, task_id))')
        connection.execute('INSERT OR IGNORE INTO metadata VALUES (?, ?)', ('recording_started', timestamp))
        connection.execute('PRAGMA user_version = 1')
        cursor = connection.execute('INSERT OR IGNORE INTO events VALUES (?, ?, ?)', (path, task_id, timestamp))
        return {'recorded': cursor.rowcount == 1, 'skill_path': path}


def summarize(skills, database=DEFAULT_DB, now=None):
    paths = [canonical(skill) for skill in skills]
    database = Path(database).expanduser()
    unknown = {path: {'total': None, 'last_30_days': None, 'last_used': None} for path in paths}
    if not database.exists():
        return {'status': 'not_recorded', 'recording_started': None, 'skills': unknown}
    current = moment(now)
    start = (current - timedelta(days=30)).isoformat(timespec='microseconds')
    end = current.isoformat(timespec='microseconds')
    with closing(sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True, timeout=10)) as connection:
        connection.execute('BEGIN')
        if connection.execute('PRAGMA user_version').fetchone()[0] != 1:
            raise ValueError('Unsupported usage database')
        row = connection.execute("SELECT value FROM metadata WHERE key='recording_started'").fetchone()
        if not row:
            raise ValueError('Missing recording scope')
        result = {}
        for path in paths:
            total, recent, last_used = connection.execute(
                'SELECT COUNT(*), COALESCE(SUM(CASE WHEN used_at >= ? THEN 1 ELSE 0 END), 0), MAX(used_at) '
                'FROM events WHERE skill_path = ? AND used_at <= ?', (start, path, end)).fetchone()
            result[path] = {'total': total, 'last_30_days': recent, 'last_used': last_used}
        return {'status': 'recorded', 'recording_started': row[0], 'skills': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='Local SQLite ledger path')
    commands = parser.add_subparsers(dest='command', required=True)
    add = commands.add_parser('record', help='Record actual execution once per skill and task')
    add.add_argument('--skill', required=True)
    add.add_argument('--task-id', required=True)
    stats = commands.add_parser('stats', help='Read counts without creating a ledger')
    stats.add_argument('skills', nargs='+')
    args = parser.parse_args()
    try:
        if args.command == 'record':
            result = record(args.skill, args.task_id, args.db)
        else:
            result = summarize(args.skills, args.db)
    except (ValueError, OSError, sqlite3.Error) as error:
        print('Usage ledger unavailable: ' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
