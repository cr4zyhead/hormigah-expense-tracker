"""
Serializers para la API REST

Este módulo contiene los serializers que convierten los modelos Django
en formato JSON para que n8n pueda consumir los datos fácilmente.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from apps.expenses.models import Expense, Budget, Category
from datetime import datetime, timedelta
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para las categorías de gastos
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'color', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer para los gastos individuales
    """
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'description', 'date', 'location', 
            'category', 'created_at', 'updated_at'
        ]


class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer para el presupuesto del usuario
    """
    class Meta:
        model = Budget
        fields = [
            'monthly_limit', 'warning_percentage', 'critical_percentage',
            'email_alerts_enabled', 'created_at', 'updated_at'
        ]


class UserActiveSerializer(serializers.ModelSerializer):
    """
    Serializer simple para la lista de usuarios activos
    Solo incluye los datos básicos que n8n necesita para iterar
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer completo para un usuario con todo su historial
    Este es el serializer principal que contiene todos los datos
    que la IA necesita para generar reportes mensuales
    """
    
    # Campos relacionados
    budget = BudgetSerializer(read_only=True)
    
    # Campos calculados (se definen en to_representation)
    complete_history = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'date_joined', 'budget', 'complete_history'
        ]
    
    def get_complete_history(self, user):
        """
        Calcula y retorna el historial completo de gastos del usuario
        
        Args:
            user: Instancia del modelo User
            
        Returns:
            dict: Historial completo con gastos, resúmenes y estadísticas
        """
        
        # Obtener todos los gastos del usuario
        expenses = Expense.objects.filter(user=user).select_related('category').order_by('-date')
        
        if not expenses.exists():
            return {
                'first_expense': None,
                'last_expense': None,
                'total_months_active': 0,
                'total_expenses': 0,
                'total_expense_count': 0,
                'all_expenses': [],
                'monthly_summaries': {},
                'categories_summary': {}
            }
        
        # Datos básicos
        first_expense = expenses.last().date
        last_expense = expenses.first().date
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        total_expense_count = expenses.count()
        
        # Calcular meses activos
        months_diff = (last_expense.year - first_expense.year) * 12 + (last_expense.month - first_expense.month)
        total_months_active = months_diff + 1
        
        # Serializar todos los gastos
        all_expenses = ExpenseSerializer(expenses, many=True).data
        
        # Calcular resúmenes mensuales
        monthly_summaries = {}
        for expense in expenses:
            month_key = f"{expense.date.year}-{expense.date.month:02d}"
            
            if month_key not in monthly_summaries:
                monthly_summaries[month_key] = {
                    'total': 0,
                    'count': 0,
                    'categories': {}
                }
            
            monthly_summaries[month_key]['total'] += float(expense.amount)
            monthly_summaries[month_key]['count'] += 1
            
            # Agrupar por categorías dentro del mes
            cat_name = expense.category.name
            if cat_name not in monthly_summaries[month_key]['categories']:
                monthly_summaries[month_key]['categories'][cat_name] = 0
            monthly_summaries[month_key]['categories'][cat_name] += float(expense.amount)
        
        # Calcular resumen por categorías (histórico total)
        categories_summary = {}
        for expense in expenses:
            cat_name = expense.category.name
            if cat_name not in categories_summary:
                categories_summary[cat_name] = {
                    'total': 0,
                    'count': 0,
                    'percentage': 0
                }
            
            categories_summary[cat_name]['total'] += float(expense.amount)
            categories_summary[cat_name]['count'] += 1
        
        # Calcular porcentajes
        for cat_name in categories_summary:
            categories_summary[cat_name]['percentage'] = round(
                (categories_summary[cat_name]['total'] / float(total_expenses)) * 100, 2
            )
        
        return {
            'first_expense': first_expense.isoformat(),
            'last_expense': last_expense.isoformat(),
            'total_months_active': total_months_active,
            'total_expenses': float(total_expenses),
            'total_expense_count': total_expense_count,
            'all_expenses': all_expenses,
            'monthly_summaries': monthly_summaries,
            'categories_summary': categories_summary
        } 