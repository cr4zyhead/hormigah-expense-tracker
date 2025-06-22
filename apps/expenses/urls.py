from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('gastos/', views.expense_list, name='expense_list'),
    path('gastos/htmx/', views.expense_list_htmx, name='expense_list_htmx'),  # Nueva ruta para HTMX
    path('agregar/', views.add_expense, name='add_expense'),
] 