from django import forms
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    """
    Formulario para crear y editar gastos
    """
    
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date', 'location']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'description': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Descripción del gasto (opcional)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Lugar (opcional)'
            }),
        }
        labels = {
            'category': 'Categoría',
            'amount': 'Cantidad (€)',
            'description': 'Descripción',
            'date': 'Fecha',
            'location': 'Lugar',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha de hoy por defecto
        if not self.instance.pk:
            from datetime import date
            self.fields['date'].initial = date.today()
        
        # Ordenar categorías por nombre
        self.fields['category'].queryset = Category.objects.all().order_by('name') 