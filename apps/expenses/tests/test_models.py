"""
Tests para los modelos de expenses

Cubre funcionalidades básicas de Category y Expense
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.expenses.models import Category, Expense


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

1. Ejecutar TODOS los tests de este archivo:
   pytest --ds=config.settings apps/expenses/tests/test_models.py -v

2. Ejecutar solo tests de Category:
   pytest --ds=config.settings apps/expenses/tests/test_models.py::TestCategoryModel -v

3. Ejecutar solo tests de Expense:
   pytest --ds=config.settings apps/expenses/tests/test_models.py::TestExpenseModel -v

4. Ejecutar un test específico:
   pytest --ds=config.settings apps/expenses/tests/test_models.py::TestExpenseModel::test_create_expense -v

5. Ejecutar con cobertura de código:
   pytest --ds=config.settings apps/expenses/tests/test_models.py --cov=apps.expenses.models -v

6. Ejecutar desde la raíz del proyecto (más rápido):
   pytest --ds=config.settings -k "test_models" -v

Nota: El parámetro --ds=config.settings es necesario para que Django configure correctamente
la base de datos y settings durante las pruebas.
""" 