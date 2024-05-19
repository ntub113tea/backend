from django.core.management.base import BaseCommand
from myapp.models import DailyCounter

class Command(BaseCommand):
    help = 'Reset daily counter for anonymous users'

    def handle(self, *args, **kwargs):
        DailyCounter.reset_counter()
        self.stdout.write(self.style.SUCCESS('Successfully reset daily counter'))
