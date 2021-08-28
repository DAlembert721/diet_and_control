from django.contrib import admin

# Register your models here.
from diets.models import Treatment, Menu, Meal, Schedule

admin.site.register(Treatment)
admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(Schedule)