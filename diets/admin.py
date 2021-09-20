from django.contrib import admin

# Register your models here.
from diets.models import Treatment, Menu, Meal, PersonalTreatment, MealSchedule, PersonalTreatmentTrace

admin.site.register(Treatment)
admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(PersonalTreatment)
admin.site.register(MealSchedule)
admin.site.register(PersonalTreatmentTrace)