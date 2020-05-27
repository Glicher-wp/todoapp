from django.core.management import BaseCommand
from tasks.models import TodoItem
from django.contrib.auth.models import User
from operator import itemgetter


class Command(BaseCommand):
    help = u"Read tasks from base and count there value from each user"

    def add_arguments(self, parser):
        parser.add_argument('--file', dest='input_file', type=str)

    def handle(self, *args, **options):
        counter = []
        is_done = 0
        else_than_20 = 0
        for u in User.objects.all():
            tc = 0
            for t in u.tasks.all():
                if not t.is_completed:
                    tc += 1
            counter.append((u, tc))

        sr = sorted(counter, key=itemgetter(1))
        print(sr[2])

        # for _, twelw_count in counter:
        #     if twelw_count < 20:
        #         else_than_20 += 1
        # print(else_than_20)

        # i = 1
        # for ut in sorted(counter, key=itemgetter(1))[::-1]:
        #     if i <= 25:
        #         print(ut)
        #         i += 1
