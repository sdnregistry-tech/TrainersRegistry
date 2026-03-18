# trainer/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from trainer.models import EmailLog

def send_expired_notice(qualification, reminder_days=0):
    """
    Sends email reminders before expiry or on expiry day.
    reminder_days = 1 -> 1-day-before reminder
    reminder_days = 0 -> expired email
    """
    today = timezone.now().date()
    trainer = qualification.trainer
    notify_date = qualification.validity_date - timezone.timedelta(days=reminder_days)

    if today != notify_date:
        return False  

    if EmailLog.objects.filter(
        trainer=trainer,
        qualification=qualification,
        sent_for_days_before=reminder_days
    ).exists():
        return False

    if reminder_days > 0:
        subject = f"Upcoming Expiration: {qualification.certificate_name}"
        message = (
            f"Dear {trainer.full_name()},\n\n"
            f"Your certificate '{qualification.certificate_name}' will expire on {qualification.validity_date}.\n"
            "Please renew it on time.\n\n"
            "Thank you,\nTESDA Office"
        )
    else:
        subject = f"Expired Certificate: {qualification.certificate_name}"
        message = (
            f"Dear {trainer.full_name()},\n\n"
            f"Your certificate '{qualification.certificate_name}' expired on {qualification.validity_date}.\n"
            "Please renew it as soon as possible.\n\n"
            "Thank you,\nTESDA Office"
        )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [trainer.email],
        fail_silently=False,
    )

    EmailLog.objects.create(
        trainer=trainer,
        qualification=qualification,
        sent_for_days_before=reminder_days
    )

    return True
