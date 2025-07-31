from django import forms
from .models import MonthlyBudget, BudgetCategory


class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['category', 'amount', 'year']


class BudgetCategoryForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = BudgetCategory
        fields = ['category', 'budget_type']
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'budget_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # CRITICAL: Always assign the user before saving
        if self.user:
            instance.user = self.user
        else:
            raise ValueError("User must be provided to save BudgetCategory")
        if commit:
            instance.save()
        return instance
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category:
            category = category.strip().title()  # Clean and format category name
            # Check for duplicate categories for this user
            if self.user:
                existing = BudgetCategory.objects.filter(
                    user=self.user, 
                    category__iexact=category,
                    is_active=True
                ).exclude(pk=self.instance.pk if self.instance else None)
                
                if existing.exists():
                    raise forms.ValidationError(
                        f"You already have a category named '{category}'"
                    )
        return category
