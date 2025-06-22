from django import forms
from .models import Expense, Category
from datetime import datetime, date, timedelta


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
            self.fields['date'].initial = date.today()
        
        # Ordenar categorías por nombre
        self.fields['category'].queryset = Category.objects.all().order_by('name') 


class ExpenseFilterForm(forms.Form):
    """
    Formulario para filtrar gastos por categoría, fecha y monto con filtros rápidos
    """
    
    # Opciones de filtros rápidos por mes
    MONTH_CHOICES = [
        ('', 'Seleccionar período'),
        ('current_month', 'Este mes'),
        ('last_month', 'Mes pasado'),
        ('current_year', 'Este año'),
        ('last_3_months', 'Últimos 3 meses'),
        ('last_6_months', 'Últimos 6 meses'),
        ('custom', 'Rango personalizado'),
    ]
    
    # Filtro rápido por período
    period = forms.ChoiceField(
        choices=MONTH_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        }),
        label="Período"
    )
    
    # Filtro por categoría
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        }),
        label="Categoría"
    )
    
    # Filtro por fecha desde
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'type': 'date'
        }),
        label="Desde"
    )
    
    # Filtro por fecha hasta
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'type': 'date'
        }),
        label="Hasta"
    )
    
    # Filtro por monto mínimo
    min_amount = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        }),
        label="Monto mínimo (€)"
    )
    
    # Filtro por monto máximo
    max_amount = forms.DecimalField(
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00'
        }),
        label="Monto máximo (€)"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar categorías por nombre
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        
    def clean(self):
        """
        Validación personalizada para asegurar coherencia en los filtros
        """
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        min_amount = cleaned_data.get('min_amount')
        max_amount = cleaned_data.get('max_amount')
        period = cleaned_data.get('period')
        
        # Si se selecciona un período predefinido, calcular las fechas
        if period and period != 'custom':
            today = date.today()
            
            if period == 'current_month':
                date_from = today.replace(day=1)
                date_to = today
            elif period == 'last_month':
                if today.month == 1:
                    date_from = date(today.year - 1, 12, 1)
                    date_to = date(today.year - 1, 12, 31)
                else:
                    date_from = date(today.year, today.month - 1, 1)
                    # Último día del mes anterior
                    next_month = date(today.year, today.month, 1)
                    date_to = next_month - timedelta(days=1)
            elif period == 'current_year':
                date_from = date(today.year, 1, 1)
                date_to = today
            elif period == 'last_3_months':
                date_from = today - timedelta(days=90)
                date_to = today
            elif period == 'last_6_months':
                date_from = today - timedelta(days=180)
                date_to = today
            
            # Actualizar los campos calculados
            cleaned_data['date_from'] = date_from
            cleaned_data['date_to'] = date_to
        
        # Validar que fecha_desde no sea mayor que fecha_hasta
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("La fecha 'desde' no puede ser mayor que la fecha 'hasta'.")
        
        # Validar que monto_mínimo no sea mayor que monto_máximo
        if min_amount and max_amount and min_amount > max_amount:
            raise forms.ValidationError("El monto mínimo no puede ser mayor que el monto máximo.")
        
        return cleaned_data 