import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils.dateparse import parse_datetime

from to_do_app.models import Task


class Command(BaseCommand):
    help = "Import Task rows from the old SQLite database without deleting existing PostgreSQL rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--sqlite-path",
            default=str(settings.BASE_DIR / "db.sqlite3"),
            help="Path to the SQLite database file to import from.",
        )

    def handle(self, *args, **options):
        sqlite_path = Path(options["sqlite_path"])
        if not sqlite_path.exists():
            self.stderr.write(self.style.ERROR(f"SQLite database not found: {sqlite_path}"))
            return

        with sqlite3.connect(sqlite_path) as sqlite_connection:
            sqlite_connection.row_factory = sqlite3.Row
            rows = sqlite_connection.execute(
                """
                SELECT id, title, description, completed, created_at, due_date
                FROM to_do_app_task
                ORDER BY id
                """
            ).fetchall()

        existing_ids = set(Task.objects.values_list("id", flat=True))
        tasks = []
        for row in rows:
            if row["id"] in existing_ids:
                continue

            tasks.append(
                Task(
                    id=row["id"],
                    title=row["title"],
                    description=row["description"],
                    completed=bool(row["completed"]),
                    created_at=parse_datetime(row["created_at"]) if row["created_at"] else None,
                    due_date=row["due_date"] or None,
                )
            )

        Task.objects.bulk_create(tasks)
        self._reset_postgres_sequence()

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(tasks)} task(s). Skipped {len(rows) - len(tasks)} existing task(s)."
            )
        )

    def _reset_postgres_sequence(self):
        if connection.vendor != "postgresql":
            return

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT setval(
                    pg_get_serial_sequence('to_do_app_task', 'id'),
                    COALESCE((SELECT MAX(id) FROM to_do_app_task), 1),
                    (SELECT COUNT(*) FROM to_do_app_task) > 0
                )
                """
            )
