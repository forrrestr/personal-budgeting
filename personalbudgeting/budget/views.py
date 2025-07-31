from django.shortcuts import render, redirect
from .models import BudgetChoices, BudgetCategory, MonthlyBudget
from .forms import MonthlyBudgetForm, BudgetCategoryForm
from django.http import HttpResponse
import csv


def budget_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=my_budget.csv'

    writer = csv.writer(response)

    budget = MonthlyBudget.objects.all() 

    writer.writerow(['category', 'year', 'month', 'amount', 'last_updated'])

    for budget in budget:
        writer.writerow([budget.category, budget.year, budget.month, budget.amount, budget.last_updated])

    return response


def budget_page(request):
    context = {}

    income_budgets = MonthlyBudget.objects.filter(category__budget_type="Income")
    context['income_budget'] = income_budgets

    expense_budgets = MonthlyBudget.objects.filter(category__budget_type="Expense")
    context['expense_budget'] = expense_budgets

    monthly_budget_form = MonthlyBudgetForm()
    context['monthly_budget_form'] = monthly_budget_form

    budget_cat_form = BudgetCategoryForm()
    context['budget_cat_form'] = budget_cat_form

    if request.method == "POST":
        if 'save' in request.POST:
            budget_id = request.POST.get('budget_id')
            if budget_id:  # Editing existing budget
                budget = MonthlyBudget.objects.get(id=budget_id)
                form = MonthlyBudgetForm(request.POST, instance=budget)
            else:  # Creating new budget
                form = MonthlyBudgetForm(request.POST)
            if form.is_valid():
                form.save()
        elif 'new-cat-save' in request.POST:
            form = BudgetCategoryForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
            else:
                pass
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            budget = MonthlyBudget.objects.get(id=pk)
            budget.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            budget = MonthlyBudget.objects.get(id=pk)
            form = MonthlyBudgetForm(instance=budget)
            context['monthly_budget_form'] = monthly_budget_form
    return render(request, 'budget/budget.html', context)
