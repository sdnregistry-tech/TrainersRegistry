from django.core.management.base import BaseCommand
from trainer.models import Trainer
from trainer.utils import send_expired_notice
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Send email to trainers if their certificate is expired or within 3 months of expiration'

    def handle(self, *args, **kwargs):
        today = date.today()
        three_months = today + timedelta(days=90)

        trainers = Trainer.objects.all()
        count = 0

        for trainer in trainers:
            for q in trainer.qualifications.all():
                if q.validity_date <= three_months:
                    send_expired_notice(
                        email=trainer.email,
                        trainer_name=f"{trainer.first_name} {trainer.last_name}",
                        certificate_name=q.certificate_name,
                        validity_date=q.validity_date.strftime("%B %d, %Y")
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Sent {count} notification(s).'))
