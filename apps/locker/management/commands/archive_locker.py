from django.core.management import BaseCommand

from apps.locker.models import rack


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        lockers = rack.objects.all()
        for locker in lockers:
            if not locker.archived:
                self.stdout.write("Locker %s archived.\n" % locker)
                locker.archived = True
                locker.save()
