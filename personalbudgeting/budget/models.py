from django.db import models
from django.contrib.auth.models import User


class BudgetChoices(models.TextChoices):
    Income = "Income"
    Expense = "Expense"


class BudgetCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=10,
                                   choices=BudgetChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category

    class Meta:
        unique_together = ['user', 'category']


MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


class MonthlyBudget(models.Model):
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 13)])
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        month = MONTHS[self.month - 1]
        return f"{month} {self.year} {self.category} -- {self.amount}"
