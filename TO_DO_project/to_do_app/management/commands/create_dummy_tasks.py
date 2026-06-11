from __future__ import annotations

from datetime import date, timedelta
from random import choice, randrange

from django.core.management.base import BaseCommand

from to_do_app.models import Task


class Command(BaseCommand):
    help = "Create 20 dummy Task records for the to_do_app."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing Task objects before creating dummy data.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Task.objects.all().delete()
            self.stdout.write(self.style.WARNING("Deleted existing Task records."))

        titles = [
            "Buy groceries",
            "Finish project report",
            "Call the bank",
            "Schedule dentist appointment",
            "Write blog post",
            "Clean the house",
            "Pay utility bills",
            "Prepare presentation",
            "Read a new book",
            "Plan weekend trip",
            "Update resume",
            "Organize desk",
            "Backup computer files",
            "Reply to emails",
            "Practice coding",
            "Exercise for 30 minutes",
            "Watch tutorial video",
            "Review team feedback",
            "Fix website bug",
            "Create meeting agenda",
        ]

        descriptions = [
            "This is a dummy task created for testing.",
            "Use this task to verify template rendering and list views.",
            "Add more details later when you work on the task.",
            "Try completing this task to test the toggle behavior.",
            "A placeholder task to fill the database with sample data.",
        ]

        created_count = 0
        for index in range(1, 21):
            title = titles[index - 1]
            Task.objects.create(
                title=title,
                description=choice(descriptions),
                completed=choice([True, False]),
                due_date=date.today() + timedelta(days=randrange(-5, 15)),
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} dummy Task records."))
