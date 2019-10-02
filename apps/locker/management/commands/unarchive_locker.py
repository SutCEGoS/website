from django.core.management import BaseCommand

from apps.locker.models import Rack


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lockers = Rack.objects.filter(archived=True)
        self.stdout.write("Start archive lockers. count: %d\n" % len(lockers))
        for locker in lockers:
            if not locker.archived:
                self.stdout.write("Locker %s archived.\n" % locker)
                locker.archived = False
                locker.save()
