# coding utf-8
from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem


class Command(BaseCommand):
    help = u"Read tasks from file (one line = one task) and save them to db"

    def add_arguments(self, parser):
        parser.add_argument('--file', dest='input_file', type=str)

    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)
        with open("input.txt", encoding='utf-8') as fp:
            for line in fp:
                task = TodoItem(description=line)
                task.save()
                print("Добавленные задачи:", task, task.created)
