from django.db import models
from datetime import date, timedelta 
from datetime import timedelta



class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
    max_length=10,
    choices=[('Male', 'Male'), ('Female', 'Female')],
    default='Male' )
    address = models.TextField()
    birthdate = models.DateField()
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def full_name(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()

class Qualification(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='qualifications')
    certificate_name = models.CharField(max_length=150, default="Qualification Title")
    nttc_number = models.CharField(max_length=100)
    validity_date = models.DateField() 

    def status(self):
        return "Active" if self.validity_date >= date.today() else "Expired"

    def __str__(self):
        return f"{self.certificate_name} ({self.nttc_number})"

    def save(self, *args, **kwargs):
        self.status = self.status()
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.certificate_name} ({self.nttc_number})"
    

    from django.db import models
from trainer.models import Trainer, Qualification

class EmailLog(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    sent_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('trainer', 'qualification')  

class EmailLog(models.Model):
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    qualification = models.ForeignKey('Qualification', on_delete=models.CASCADE)
    sent_on = models.DateField(auto_now_add=True)
    sent_for_days_before = models.IntegerField(default=0)  # 1 = reminder, 0 = expired email

    class Meta:
        unique_together = ('trainer', 'qualification', 'sent_for_days_before')
