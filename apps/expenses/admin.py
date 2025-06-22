from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin para gestionar categorías de gastos"""
    list_display = ['name', 'icon', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    fields = ['name', 'icon', 'color', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin para gestionar gastos individuales"""
    list_display = ['date', 'amount', 'category', 'user', 'description']
    list_filter = ['category', 'date', 'user', 'created_at']
    search_fields = ['description', 'location']
    ordering = ['-date', '-created_at']  
    date_hierarchy = 'date'
    fields = ['user', 'category', 'amount', 'date', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['category']  # Para búsqueda rápida
