from django.core.management import BaseCommand

from apps.locker.models import rack


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lockers = rack.objects.filter(archived=False)
        self.stdout.write("Start archive lockers. count: %d\n" % len(lockers))
        for locker in lockers:
            if not locker.archived:
                self.stdout.write("Locker %s archived.\n" % locker)
                locker.archived = True
                locker.save()
