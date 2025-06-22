from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"{self.amount}€ - {self.category.name} ({self.date})"
