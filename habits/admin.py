from django.contrib import admin

# Register your models here.
from habits.models import HarmfulHabit, PhysicalActivity

admin.site.register(HarmfulHabit)
admin.site.register(PhysicalActivity)