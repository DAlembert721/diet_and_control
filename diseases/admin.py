from django.contrib import admin

# Register your models here.
from diseases.models import Illness, FamiliarIllness

admin.site.register(Illness)
admin.site.register(FamiliarIllness)