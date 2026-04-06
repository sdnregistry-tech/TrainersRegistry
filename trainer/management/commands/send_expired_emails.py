
from django.core.management.base import BaseCommand
from django.utils import timezone
from trainer.models import Qualification
from trainer.utils import send_expired_notice

class Command(BaseCommand):
    help = "Send 1-day-before reminders and expired emails for qualifications"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        tomorrow = today + timezone.timedelta(days=1)

        qualifications = Qualification.objects.filter(validity_date__in=[today, tomorrow])

        for q in qualifications:

            if send_expired_notice(q, reminder_days=1):
                self.stdout.write(
                    f"1-day-before reminder sent to {q.trainer.full_name()} ({q.trainer.email})"
                )

            if send_expired_notice(q, reminder_days=0):
                self.stdout.write(
                    f"Expired email sent to {q.trainer.full_name()} ({q.trainer.email})"
                )
