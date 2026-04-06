
from django.db.models.signals import post_save
from django.dispatch import receiver
from trainer.models import Qualification
from trainer.utils import send_expired_notice
from django.utils import timezone

@receiver(post_save, sender=Qualification)
def send_reminder_90_days_before(sender, instance, created, **kwargs):
    """
    Automatically sends:
    - 90-day-before reminders
    - Expired emails on the expiry date
    when a Qualification is created or updated.
    """
    today = timezone.now().date()
    expiry_date = instance.validity_date

    if expiry_date - timezone.timedelta(days=90) == today:
        sent = send_expired_notice(instance, reminder_days=90)
        if sent:
            print(f"90-day-before reminder sent to {instance.trainer.full_name()} ({instance.trainer.email})")

    if expiry_date == today:
        sent = send_expired_notice(instance, reminder_days=0)
        if sent:
            print(f"Expired email sent to {instance.trainer.full_name()} ({instance.trainer.email})")
