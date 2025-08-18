from django.contrib import admin
from .models import Calculation

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ("user", "expression", "result", "timestamp")
    list_filter = ("user", "timestamp")
