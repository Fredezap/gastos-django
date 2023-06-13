from django.forms import ModelForm
from django import forms
from .models import Movements, Category

class MovementsPaymentForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_payment=True), label='Categoria', widget=forms.Select(attrs={'class': 'category-select'}))
    class Meta:
        model = Movements
        exclude = ('total_amount', 'salary_funds_before', 'still_exist', 'is_savings_withdraw',
                'salary_funds_after', 'savings_funds_before', 'savings_funds_after', 'date')
        labels = {
            'amount': 'Monto',
            'savings': 'Ahorro',
            'payment_method': 'Metodo de pago',
            'detail': 'Detalle',
        }

class MovementsFundsForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_payment=False), label='Categoria')
    class Meta:
        model = Movements
        exclude = ('total_amount', 'salary_funds_before', 'still_exist', 'savings', 'is_savings_withdraw',
                'salary_funds_after', 'savings_funds_before', 'savings_funds_after', 'date')
        labels = {
            'amount': 'Monto',
            'payment_method': 'Metodo de pago',
            'detail': 'Detalle',
        }

class SavingsDepositForm(ModelForm):
    class Meta:
        model = Movements
        fields = ('savings', 'detail',)
        labels = {
            'savings': 'Monto',
            'detail': 'Detalle',
        }
        
class SavingsWithdrawForm(ModelForm):
    class Meta:
        model = Movements
        fields = ('amount', 'detail',)
        labels = {
            'amount': 'Monto',
            'detail': 'Detalle',
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('last_funds', 'current_funds', 'still_exist')
        labels = {
            'name': 'Nombre',
            'detail': 'Detalle',
            'percentage': 'Porcentaje',
            'goal_founds': 'Objetivo ahorro',
            'is_payment': 'Es pago?',
        }
