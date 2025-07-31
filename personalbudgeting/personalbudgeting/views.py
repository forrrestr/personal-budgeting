from django.shortcuts import render
from budget.models import MonthlyBudget
from django.db.models import Sum


def homepage(request):

    context = {}

    totat_income_budget = MonthlyBudget.objects.filter(category__budget_type="Income").aggregate(total=Sum('amount'))['total'] or 0
    context['totat_income_budget'] = totat_income_budget

    total_expense_budget = MonthlyBudget.objects.filter(category__budget_type="Expense").aggregate(total=Sum('amount'))['total'] or 0
    context['total_expense_budget'] = total_expense_budget
    context['totat_budget'] = totat_income_budget - total_expense_budget

    return render(request, 'home.html', context)


def help(request):
    return render(request, 'help.html')
