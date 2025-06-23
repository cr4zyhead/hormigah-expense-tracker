"""
Tests para las utilidades de expenses

Cubre funciones críticas de dashboard, filtros y CRUD
"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from apps.expenses.models import Category, Expense
from apps.expenses.utils.util_dashboard import (
    get_period_dates, 
    calculate_dashboard_metrics
)
from apps.expenses.utils.util_expense_list import (
    calculate_expense_statistics,
    detect_active_filters
)
from apps.expenses.utils.util_crud_operations import (
    get_expense_for_user,
    handle_expense_creation
)
from apps.expenses.forms import ExpenseForm, ExpenseFilterForm


class TestDashboardUtils:
    """Tests para utilidades del dashboard"""
    
    def test_get_period_dates_current_month(self):
        """Test cálculo de fechas para mes actual"""
        start_date, end_date, period_label = get_period_dates('current_month')
        
        today = datetime.now().date()
        expected_start = today.replace(day=1)
        
        assert start_date == expected_start
        assert start_date.day == 1
        assert end_date.month == today.month
        assert "Este mes" in period_label
    
    def test_get_period_dates_last_7_days(self):
        """Test cálculo de fechas para últimos 7 días"""
        start_date, end_date, period_label = get_period_dates('last_7_days')
        
        today = datetime.now().date()
        expected_start = today - timedelta(days=7)
        
        assert start_date == expected_start
        assert end_date == today
        assert period_label == "Últimos 7 días"
    
    def test_get_period_dates_default(self):
        """Test comportamiento por defecto (mes actual)"""
        start_date, end_date, period_label = get_period_dates('invalid_period')
        
        today = datetime.now().date()
        expected_start = today.replace(day=1)
        
        assert start_date == expected_start
        assert "Este mes" in period_label

    @pytest.mark.django_db
    def test_calculate_dashboard_metrics(self):
        """Test cálculo de métricas del dashboard"""
        # Crear datos de test
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        # Crear gastos para el período
        today = date.today()
        start_date = today.replace(day=1)
        end_date = today
        
        Expense.objects.create(
            user=user, category=category, 
            amount=Decimal('10.00'), date=today
        )
        Expense.objects.create(
            user=user, category=category, 
            amount=Decimal('20.00'), date=today
        )
        
        # Calcular métricas
        metrics = calculate_dashboard_metrics(user, start_date, end_date)
        
        assert metrics['period_total'] == Decimal('30.00')
        assert metrics['period_expenses_count'] == 2
        assert metrics['period_avg_daily'] > 0
        assert 'recent_expenses' in metrics
        assert 'categories_summary' in metrics


class TestExpenseListUtils:
    """Tests para utilidades de lista de gastos"""
    
    def test_calculate_expense_statistics_empty(self):
        """Test estadísticas con QuerySet vacío"""
        from django.db.models import QuerySet
        from apps.expenses.models import Expense
        
        empty_queryset = Expense.objects.none()
        stats = calculate_expense_statistics(empty_queryset)
        
        assert stats['total_filtered'] == 0
        assert stats['count_filtered'] == 0
    
    @pytest.mark.django_db
    def test_calculate_expense_statistics_with_data(self):
        """Test estadísticas con datos reales"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        # Crear gastos
        Expense.objects.create(
            user=user, category=category, amount=Decimal('15.00'), date=date.today()
        )
        Expense.objects.create(
            user=user, category=category, amount=Decimal('25.00'), date=date.today()
        )
        
        expenses = Expense.objects.filter(user=user)
        stats = calculate_expense_statistics(expenses)
        
        assert stats['total_filtered'] == Decimal('40.00')
        assert stats['count_filtered'] == 2
    
    def test_detect_active_filters_empty_form(self):
        """Test detección con formulario vacío"""
        form = ExpenseFilterForm({})
        
        has_filters = detect_active_filters(form)
        assert has_filters is False
    
    def test_detect_active_filters_with_data(self):
        """Test detección con filtros activos"""
        form_data = {
            'period': 'current_month',
            'min_amount': '10.00'
        }
        form = ExpenseFilterForm(form_data)
        
        has_filters = detect_active_filters(form)
        assert has_filters is True


class TestCrudOperations:
    """Tests para operaciones CRUD"""
    
    @pytest.mark.django_db
    def test_get_expense_for_user_success(self):
        """Test obtener gasto que pertenece al usuario"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        expense = Expense.objects.create(
            user=user, category=category, amount=Decimal('15.00'), date=date.today()
        )
        
        retrieved_expense = get_expense_for_user(expense.id, user)
        assert retrieved_expense == expense
    
    @pytest.mark.django_db
    def test_get_expense_for_user_not_owner(self):
        """Test obtener gasto que NO pertenece al usuario"""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        expense = Expense.objects.create(
            user=user1, category=category, amount=Decimal('15.00'), date=date.today()
        )
        
        with pytest.raises(Expense.DoesNotExist):
            get_expense_for_user(expense.id, user2)
    
    @pytest.mark.django_db
    def test_handle_expense_creation_valid(self):
        """Test creación exitosa de gasto"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        form_data = {
            'category': category.id,
            'amount': '25.50',
            'description': 'Test expense',
            'date': date.today()
        }
        
        expense, form, is_valid = handle_expense_creation(form_data, user)
        
        assert is_valid is True
        assert expense is not None
        assert expense.user == user
        assert expense.amount == Decimal('25.50')
    
    @pytest.mark.django_db 
    def test_handle_expense_creation_invalid(self):
        """Test creación fallida por datos inválidos"""
        user = User.objects.create_user(username="testuser")
        
        form_data = {
            'amount': 'invalid_amount',  # Inválido
            'description': 'Test expense'
        }
        
        expense, form, is_valid = handle_expense_creation(form_data, user)
        
        assert is_valid is False
        assert expense is None
        assert form.errors  # Debe tener errores 


# =============================================================================
# CÓMO EJECUTAR ESTOS TESTS
# =============================================================================
"""
Para ejecutar los tests de utilidades, usa estos comandos:

1. Ejecutar TODOS los tests de este archivo:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py -v

2. Ejecutar solo tests de Dashboard:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py::TestDashboardUtils -v

3. Ejecutar solo tests de ExpenseList:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py::TestExpenseListUtils -v

4. Ejecutar solo tests de CRUD Operations:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py::TestCrudOperations -v

5. Ejecutar un test específico:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py::TestDashboardUtils::test_calculate_dashboard_metrics -v

6. Ejecutar solo tests que usan la base de datos:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py -m django_db -v

7. Ejecutar con cobertura de las utilidades:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py --cov=apps.expenses.utils -v

8. Ejecutar desde la raíz del proyecto (más rápido):
   pytest --ds=config.settings -k "test_utils" -v

Consejos útiles:
- Usa -v para output verbose (más detalles)
- Usa -s para ver prints de debug
- Usa --tb=short para stack traces más cortos
- Usa -x para parar en el primer fallo

Ejemplo completo con todas las opciones:
pytest --ds=config.settings apps/expenses/tests/test_utils.py -v -s --tb=short --cov=apps.expenses.utils
""" 