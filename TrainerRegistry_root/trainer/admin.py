from django.contrib import admin
from .models import Trainer
from .models import Qualification

admin.site.register(Qualification)



@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name","middle_name","last_name", "gender", "address", "birthdate", "email","contact_number"]




