"""
Tests para los modelos de expenses

Cubre funcionalidades básicas de Category y Expense
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.expenses.models import Category, Expense, Budget


@pytest.mark.django_db
class TestCategoryModel:
    """Tests para el modelo Category"""
    
    def test_create_category(self):
        """Test básico de creación de categoría"""
        category = Category.objects.create(
            name="Test Category",
            color="#FF0000"
        )
        assert category.name == "Test Category"
        assert category.color == "#FF0000"
        assert str(category) == "Test Category"
    
    def test_category_str_representation(self):
        """Test del método __str__ de Category"""
        category = Category(name="Café")
        assert str(category) == "Café"
    
    def test_category_unique_name(self):
        """Test que el nombre de categoría sea único"""
        Category.objects.create(name="Café", color="#8B4513")
        
        with pytest.raises(Exception):  # IntegrityError por unique constraint
            Category.objects.create(name="Café", color="#FF0000")


@pytest.mark.django_db
class TestExpenseModel:
    """Tests para el modelo Expense"""
    
    def test_create_expense(self):
        """Test básico de creación de gasto"""
        # Crear usuario y categoría
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        category = Category.objects.create(
            name="Test Category",
            color="#FF0000"
        )
        
        # Crear gasto
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=Decimal('15.50'),
            description="Test expense",
            date=date.today()
        )
        
        assert expense.user == user
        assert expense.category == category
        assert expense.amount == Decimal('15.50')
        assert expense.description == "Test expense"
        assert expense.date == date.today()
    
    def test_expense_str_representation(self):
        """Test del método __str__ de Expense"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Café", color="#8B4513")
        
        expense_date = date.today()
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=Decimal('5.00'),
            description="Café matutino",
            date=expense_date
        )
        
        expected_str = f"{expense.amount}€ - Café ({expense_date})"
        assert str(expense) == expected_str
    
    def test_expense_without_description(self):
        """Test de gasto sin descripción"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Café", color="#8B4513")
        
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=Decimal('5.00'),
            date=date.today()
            # Sin descripción
        )
        
        assert expense.description is None or expense.description == ""
    
    def test_expense_amount_validation(self):
        """Test de validación de amount positivo"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        # Amount debe ser positivo
        expense = Expense(
            user=user,
            category=category,
            amount=Decimal('-5.00'),  # Negativo
            description="Test",
            date=date.today()
        )
        
        with pytest.raises(ValidationError):
            expense.full_clean()
    
    def test_expense_ordering(self):
        """Test del ordenamiento por defecto de gastos"""
        user = User.objects.create_user(username="testuser")
        category = Category.objects.create(name="Test", color="#FF0000")
        
        # Crear múltiples gastos con fechas diferentes
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        expense1 = Expense.objects.create(
            user=user, category=category, amount=Decimal('10.00'), date=two_days_ago
        )
        expense2 = Expense.objects.create(
            user=user, category=category, amount=Decimal('20.00'), date=yesterday
        )
        expense3 = Expense.objects.create(
            user=user, category=category, amount=Decimal('30.00'), date=today
        )
        
        # Verificar orden (más recientes primero por defecto en Meta)
        expenses = list(Expense.objects.all())
        assert expenses[0] == expense3  # Más reciente (hoy)
        assert expenses[1] == expense2  # Ayer
        assert expenses[2] == expense1  # Hace dos días


# =============================================================================
# CÓMO EJECUTAR ESTOS TESTS
# =============================================================================
"""
Para ejecutar los tests de modelos, usa estos comandos:

** SI USAS DOCKER (recomendado), añade 'docker compose exec web' antes de cada comando **

1. Ejecutar TODOS los tests de este archivo:
   docker compose exec web pytest apps/expenses/tests/test_models.py -v

2. Ejecutar solo tests de Category:
   docker compose exec web pytest apps/expenses/tests/test_models.py::TestCategoryModel -v

3. Ejecutar solo tests de Expense:
   docker compose exec web pytest apps/expenses/tests/test_models.py::TestExpenseModel -v

4. Ejecutar solo tests de Budget:
   docker compose exec web pytest apps/expenses/tests/test_models.py::TestBudgetModel -v

5. Ejecutar un test específico:
   docker compose exec web pytest apps/expenses/tests/test_models.py::TestBudgetModel::test_create_budget -v

6. Ejecutar con cobertura de código:
   docker compose exec web pytest apps/expenses/tests/test_models.py --cov=apps.expenses.models -v

7. Ejecutar desde la raíz del proyecto (más rápido):
   docker compose exec web pytest -k "test_models" -v

** SI NO USAS DOCKER, añade '--ds=config.settings' a cada comando **

Ejemplo sin Docker:
   pytest --ds=config.settings apps/expenses/tests/test_models.py -v

Nota: Con Docker no necesitas --ds=config.settings porque la configuración ya está establecida.
"""


@pytest.mark.django_db
class TestBudgetModel:
    """Tests para el modelo Budget"""
    
    def test_create_budget(self):
        """Test básico de creación de presupuesto"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('500.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        assert budget.user == user
        assert budget.monthly_limit == Decimal('500.00')
        assert budget.warning_percentage == 75
        assert budget.critical_percentage == 90
    
    def test_budget_str_representation(self):
        """Test del método __str__ de Budget"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00')
        )
        
        expected_str = f"Presupuesto de testuser: €1000.00/mes"
        assert str(budget) == expected_str
    
    def test_budget_one_to_one_constraint(self):
        """Test que cada usuario solo puede tener un presupuesto"""
        user = User.objects.create_user(username="testuser")
        
        # Crear primer presupuesto
        Budget.objects.create(
            user=user,
            monthly_limit=Decimal('500.00')
        )
        
        # Intentar crear segundo presupuesto para el mismo usuario
        with pytest.raises(Exception):  # IntegrityError por OneToOneField
            Budget.objects.create(
                user=user,
                monthly_limit=Decimal('1000.00')
            )
    
    def test_budget_validation_positive_limit(self):
        """Test validación de límite positivo"""
        user = User.objects.create_user(username="testuser")
        
        budget = Budget(
            user=user,
            monthly_limit=Decimal('-100.00'),  # Negativo
            warning_percentage=75,
            critical_percentage=90
        )
        
        with pytest.raises(ValidationError):
            budget.full_clean()
    
    def test_budget_validation_percentage_order(self):
        """Test validación que warning < critical"""
        user = User.objects.create_user(username="testuser")
        
        budget = Budget(
            user=user,
            monthly_limit=Decimal('500.00'),
            warning_percentage=95,  # Mayor que critical
            critical_percentage=90
        )
        
        with pytest.raises(ValidationError):
            budget.full_clean()
    
    def test_get_warning_amount(self):
        """Test cálculo del monto de alerta amarilla"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75
        )
        
        warning_amount = budget.get_warning_amount()
        assert warning_amount == Decimal('750.00')  # 75% de 1000
    
    def test_get_critical_amount(self):
        """Test cálculo del monto de alerta roja"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            critical_percentage=90
        )
        
        critical_amount = budget.get_critical_amount()
        assert critical_amount == Decimal('900.00')  # 90% de 1000
    
    def test_get_percentage_used_normal(self):
        """Test cálculo de porcentaje usado - caso normal"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00')
        )
        
        percentage = budget.get_percentage_used(Decimal('250.00'))
        assert percentage == 25.0  # 250/1000 * 100
    
    def test_get_percentage_used_over_limit(self):
        """Test cálculo de porcentaje usado - sobre el límite"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00')
        )
        
        percentage = budget.get_percentage_used(Decimal('1500.00'))
        assert percentage == 100.0  # Máximo 100% aunque sea más
    
    def test_get_percentage_used_zero_limit(self):
        """Test cálculo de porcentaje con límite cero"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('0.00')
        )
        
        percentage = budget.get_percentage_used(Decimal('100.00'))
        assert percentage == 0  # Protección contra división por cero
    
    def test_get_remaining_amount_positive(self):
        """Test cálculo de monto restante - caso positivo"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00')
        )
        
        remaining = budget.get_remaining_amount(Decimal('300.00'))
        assert remaining == Decimal('700.00')  # 1000 - 300
    
    def test_get_remaining_amount_exceeded(self):
        """Test cálculo de monto restante - límite excedido"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00')
        )
        
        remaining = budget.get_remaining_amount(Decimal('1200.00'))
        assert remaining == 0  # Nunca negativo
    
    def test_get_status_for_amount_safe(self):
        """Test estado 'safe' - gasto bajo"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        status = budget.get_status_for_amount(Decimal('500.00'))  # 50%
        assert status == 'safe'
    
    def test_get_status_for_amount_warning(self):
        """Test estado 'warning' - alerta amarilla"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        status = budget.get_status_for_amount(Decimal('800.00'))  # 80%
        assert status == 'warning'
    
    def test_get_status_for_amount_critical(self):
        """Test estado 'critical' - alerta roja"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        status = budget.get_status_for_amount(Decimal('950.00'))  # 95%
        assert status == 'critical'
    
    def test_get_status_for_amount_exceeded(self):
        """Test estado 'exceeded' - límite superado"""
        user = User.objects.create_user(username="testuser")
        budget = Budget.objects.create(
            user=user,
            monthly_limit=Decimal('1000.00'),
            warning_percentage=75,
            critical_percentage=90
        )
        
        status = budget.get_status_for_amount(Decimal('1100.00'))  # 110%
        assert status == 'exceeded' 