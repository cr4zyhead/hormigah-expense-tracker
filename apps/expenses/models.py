from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Categorías de gastos: café, delivery, transporte, etc."""
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    icon = models.CharField(max_length=50, verbose_name="Icono")
    color = models.CharField(max_length=7, verbose_name="Color")  # Formato hexadecimal
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    """Gasto individual registrado por el usuario"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Si se borra el usuario, se borran sus gastos
        verbose_name="Usuario",
        related_name="expenses"
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,  # No se puede borrar categoría con gastos
        verbose_name="Categoría",
        related_name="expenses"
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,  # DecimalField es mejor que FloatField para dinero
        verbose_name="Cantidad"
    )
    
    description = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Descripción"
    )
    
    date = models.DateField(verbose_name="Fecha")
    location = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        verbose_name="Ubicación"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ['-date', '-created_at']  # Más recientes primero

    def clean(self):
        """Validaciones personalizadas del modelo"""
        super().clean()
        if self.amount and self.amount <= 0:
            raise ValidationError({
                'amount': 'El monto debe ser mayor que cero.'
            })

    def __str__(self):
        return f"{self.amount}€ - {self.category.name} ({self.date})"


class Budget(models.Model):
    """Límite de presupuesto del usuario para controlar gastos"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        related_name="budget"
    )
    
    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Límite Mensual",
        help_text="Límite máximo de gastos por mes en euros"
    )
    
    # Configuración de alertas
    warning_percentage = models.PositiveIntegerField(
        default=75,
        verbose_name="Porcentaje de Alerta",
        help_text="Porcentaje del límite para mostrar alerta amarilla (ej: 75)"
    )
    
    critical_percentage = models.PositiveIntegerField(
        default=90,
        verbose_name="Porcentaje Crítico",
        help_text="Porcentaje del límite para mostrar alerta roja (ej: 90)"
    )
    
    # Configuración de notificaciones por email
    email_alerts_enabled = models.BooleanField(
        default=False,
        verbose_name="Alertas por Email",
        help_text="Recibir notificaciones por email al superar el porcentaje crítico"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    
    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"
    
    def clean(self):
        """Validaciones personalizadas del modelo"""
        super().clean()
        if self.monthly_limit and self.monthly_limit <= 0:
            raise ValidationError({
                'monthly_limit': 'El límite mensual debe ser mayor que cero.'
            })
        
        if self.warning_percentage >= self.critical_percentage:
            raise ValidationError({
                'warning_percentage': 'El porcentaje de alerta debe ser menor que el crítico.'
            })
    
    def get_warning_amount(self):
        """Calcula el monto de alerta amarilla"""
        return (self.monthly_limit * self.warning_percentage) / 100
    
    def get_critical_amount(self):
        """Calcula el monto de alerta roja"""
        return (self.monthly_limit * self.critical_percentage) / 100
    
    def get_status_for_amount(self, current_amount):
        """
        Retorna el estado del presupuesto basado en el monto actual
        
        Returns:
            str: 'safe', 'warning', 'critical', 'exceeded'
        """
        if current_amount >= self.monthly_limit:
            return 'exceeded'
        elif current_amount >= self.get_critical_amount():
            return 'critical'
        elif current_amount >= self.get_warning_amount():
            return 'warning'
        else:
            return 'safe'
    
    def get_percentage_used(self, current_amount):
        """Calcula el porcentaje usado del presupuesto"""
        if self.monthly_limit <= 0:
            return 0
        return min(100, (current_amount / self.monthly_limit) * 100)
    
    def get_remaining_amount(self, current_amount):
        """Calcula el monto restante del presupuesto"""
        return max(0, self.monthly_limit - current_amount)
    
    def __str__(self):
        return f"Presupuesto de {self.user.username}: €{self.monthly_limit}/mes"
