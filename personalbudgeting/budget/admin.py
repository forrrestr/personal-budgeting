from django.contrib import admin
from .models import BudgetChoices, BudgetCategory, MonthlyBudget

# Register your models here.
admin.site.register(BudgetCategory)
admin.site.register(MonthlyBudget)

