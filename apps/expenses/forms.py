from django import forms
from .models import Expense, Category, Budget
from datetime import datetime, date, timedelta


class DateInput(forms.DateInput):
    """
    Widget personalizado para fechas que funciona correctamente con HTML5
    """
    input_type = 'date'
    
    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        return value.strftime('%Y-%m-%d') if value else ''


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
            'date': DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
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


class BudgetForm(forms.ModelForm):
    """
    Formulario para configurar el presupuesto mensual del usuario
    """
    
    class Meta:
        model = Budget
        fields = ['monthly_limit', 'warning_percentage', 'critical_percentage', 'email_alerts_enabled']
        widgets = {
            'monthly_limit': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'step': '0.01',
                'min': '0',
                'placeholder': '500.00'
            }),
            'warning_percentage': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '1',
                'max': '100',
                'placeholder': '75'
            }),
            'critical_percentage': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'min': '1',
                'max': '100',
                'placeholder': '90'
            }),
        }
        labels = {
            'monthly_limit': 'Límite Mensual (€)',
            'warning_percentage': 'Alerta Amarilla (%)',
            'critical_percentage': 'Alerta Roja (%)',
        }
        help_texts = {
            'monthly_limit': 'Establece tu límite máximo de gastos por mes',
            'warning_percentage': 'Porcentaje del límite para mostrar alerta amarilla (recomendado: 75%)',
            'critical_percentage': 'Porcentaje del límite para mostrar alerta roja (recomendado: 90%)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Valores por defecto inteligentes
        if not self.instance.pk:
            self.fields['warning_percentage'].initial = 75
            self.fields['critical_percentage'].initial = 90
    
    def clean(self):
        """
        Validación personalizada para el formulario de presupuesto
        """
        cleaned_data = super().clean()
        monthly_limit = cleaned_data.get('monthly_limit')
        warning_percentage = cleaned_data.get('warning_percentage')
        critical_percentage = cleaned_data.get('critical_percentage')
        
        # Validar que el límite mensual sea positivo
        if monthly_limit and monthly_limit <= 0:
            raise forms.ValidationError({
                'monthly_limit': 'El límite mensual debe ser mayor que cero.'
            })
        
        # Validar que warning_percentage sea menor que critical_percentage
        if warning_percentage and critical_percentage:
            if warning_percentage >= critical_percentage:
                raise forms.ValidationError({
                    'warning_percentage': 'El porcentaje de alerta debe ser menor que el crítico.'
                })
        
        # Validar rangos de porcentajes
        if warning_percentage and (warning_percentage < 1 or warning_percentage > 100):
            raise forms.ValidationError({
                'warning_percentage': 'El porcentaje debe estar entre 1 y 100.'
            })
        
        if critical_percentage and (critical_percentage < 1 or critical_percentage > 100):
            raise forms.ValidationError({
                'critical_percentage': 'El porcentaje debe estar entre 1 y 100.'
            })
        
        return cleaned_data 