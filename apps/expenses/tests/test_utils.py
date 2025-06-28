"""
Tests para las utilidades de expenses

Cubre funciones críticas de dashboard, filtros y CRUD
"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from apps.expenses.models import Category, Expense, Budget
from apps.expenses.utils.util_dashboard import (
    get_period_dates, 
    calculate_dashboard_metrics,
    get_budget_info
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


class TestBudgetUtils:
    """Tests para utilidades de presupuesto"""
    
    @pytest.mark.django_db
    def test_get_budget_info_no_budget(self):
        """Test get_budget_info cuando el usuario no tiene presupuesto"""
        user = User.objects.create_user(username="testuser")
        
        budget_info = get_budget_info(user, Decimal('500.00'))
        
        assert budget_info['has_budget'] is False
        assert budget_info['budget'] is None
    
    @pytest.mark.django_db
    def test_get_budget_info_safe_status(self):
        """Test get_budget_info con estado 'safe'"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        current_amount = Decimal('500.00')  # 50% del límite
        budget_info = get_budget_info(user, current_amount)
        
        assert budget_info['has_budget'] is True
        assert budget_info['budget'] == budget
        assert budget_info['budget_status'] == 'safe'
        assert budget_info['budget_percentage_used'] == 50.0
        assert budget_info['budget_remaining'] == Decimal('500.00')
        assert '✅' in budget_info['budget_icon']
        assert 'text-green-600' in budget_info['budget_color_class']
        assert '¡Vas bien!' in budget_info['budget_message']
    
    @pytest.mark.django_db
    def test_get_budget_info_warning_status(self):
        """Test get_budget_info con estado 'warning'"""
        user = User.objects.create_user(username="testuser")
        Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        current_amount = Decimal('800.00')  # 80% del límite
        budget_info = get_budget_info(user, current_amount)
        
        assert budget_info['budget_status'] == 'warning'
        assert budget_info['budget_percentage_used'] == 80.0
        assert budget_info['budget_remaining'] == Decimal('200.00')
        assert '⚠️' in budget_info['budget_icon']
        assert 'text-yellow-600' in budget_info['budget_color_class']
        assert '¡Cuidado!' in budget_info['budget_message']
    
    @pytest.mark.django_db
    def test_get_budget_info_critical_status(self):
        """Test get_budget_info con estado 'critical'"""
        user = User.objects.create_user(username="testuser")
        Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        current_amount = Decimal('950.00')  # 95% del límite
        budget_info = get_budget_info(user, current_amount)
        
        assert budget_info['budget_status'] == 'critical'
        assert budget_info['budget_percentage_used'] == 95.0
        assert budget_info['budget_remaining'] == Decimal('50.00')
        assert '🚨' in budget_info['budget_icon']
        assert 'text-red-600' in budget_info['budget_color_class']
        assert '¡Límite casi alcanzado!' in budget_info['budget_message']
    
    @pytest.mark.django_db
    def test_get_budget_info_exceeded_status(self):
        """Test get_budget_info con estado 'exceeded'"""
        user = User.objects.create_user(username="testuser")
        Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        current_amount = Decimal('1200.00')  # 120% del límite
        budget_info = get_budget_info(user, current_amount)
        
        assert budget_info['budget_status'] == 'exceeded'
        assert budget_info['budget_percentage_used'] == 100.0  # Máximo 100%
        assert budget_info['budget_remaining'] == 0
        assert '🛑' in budget_info['budget_icon']
        assert 'text-red-600' in budget_info['budget_color_class']
        assert '¡Límite excedido!' in budget_info['budget_message']
        assert '€200' in budget_info['budget_message']  # Exceso calculado
    
    @pytest.mark.django_db
    def test_get_budget_info_custom_percentages(self):
        """Test get_budget_info con porcentajes personalizados"""
        user = User.objects.create_user(username="testuser")
        Budget.objects.create(
            user=user,
            monthly_limit=Decimal('2000.00'),
            warning_percentage=60,  # Personalizado
            critical_percentage=80  # Personalizado
        )
        
        # Test alerta amarilla con porcentajes personalizados
        current_amount = Decimal('1400.00')  # 70% del límite
        budget_info = get_budget_info(user, current_amount)
        
        assert budget_info['budget_status'] == 'warning'  # Entre 60% y 80%
        assert budget_info['budget_percentage_used'] == 70.0


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

** SI USAS DOCKER (recomendado), añade 'docker compose exec web' antes de cada comando **

1. Ejecutar TODOS los tests de este archivo:
   docker compose exec web pytest apps/expenses/tests/test_utils.py -v

2. Ejecutar solo tests de Dashboard:
   docker compose exec web pytest apps/expenses/tests/test_utils.py::TestDashboardUtils -v

3. Ejecutar solo tests de Budget:
   docker compose exec web pytest apps/expenses/tests/test_utils.py::TestBudgetUtils -v

4. Ejecutar solo tests de ExpenseList:
   docker compose exec web pytest apps/expenses/tests/test_utils.py::TestExpenseListUtils -v

5. Ejecutar solo tests de CRUD Operations:
   docker compose exec web pytest apps/expenses/tests/test_utils.py::TestCrudOperations -v

6. Ejecutar un test específico:
   docker compose exec web pytest apps/expenses/tests/test_utils.py::TestBudgetUtils::test_get_budget_info_safe_status -v

7. Ejecutar solo tests que usan la base de datos:
   docker compose exec web pytest apps/expenses/tests/test_utils.py -m django_db -v

8. Ejecutar con cobertura de las utilidades:
   docker compose exec web pytest apps/expenses/tests/test_utils.py --cov=apps.expenses.utils -v

9. Ejecutar desde la raíz del proyecto (más rápido):
   docker compose exec web pytest -k "test_utils" -v

** SI NO USAS DOCKER, añade '--ds=config.settings' a cada comando **

Ejemplo sin Docker:
   pytest --ds=config.settings apps/expenses/tests/test_utils.py -v

Consejos útiles:
- Usa -v para output verbose (más detalles)
- Usa -s para ver prints de debug
- Usa --tb=short para stack traces más cortos
- Usa -x para parar en el primer fallo

Ejemplo completo con todas las opciones:
docker compose exec web pytest apps/expenses/tests/test_utils.py -v -s --tb=short --cov=apps.expenses.utils

Nota: Con Docker no necesitas --ds=config.settings porque la configuración ya está establecida.
""" 