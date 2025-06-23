from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm
from .utils import (
    get_dashboard_context, 
    get_expense_list_context,
    get_expense_for_user,
    handle_expense_form_update,
    build_expense_edit_context,
    handle_expense_error_response,
    create_htmx_edit_response,
    # Nuevas funciones para add_expense
    handle_expense_creation,
    create_htmx_add_response,
    build_add_expense_context,
    # Nuevas funciones para delete_expense
    handle_expense_deletion,
    build_delete_success_context,
    create_htmx_delete_response
)


@login_required
def dashboard(request):
    """
    Vista del dashboard refactorizada - limpia y enfocada
    Maneja filtros de período con HTMX
    """
    # Obtener el período seleccionado del filtro
    period = request.GET.get('period', 'current_month')
    
    # Obtener todo el contexto del dashboard usando las funciones auxiliares
    context = get_dashboard_context(request.user, period)
    
    # Si es una petición HTMX, devolver solo las métricas
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/dashboard_metrics.html', context)
    
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list(request):
    """
    Vista refactorizada - limpia y profesional
    Maneja tanto peticiones normales como HTMX usando funciones auxiliares
    """
    # Obtener todo el contexto usando las funciones auxiliares
    context = get_expense_list_context(request.user, request.GET)
    
    # ¿Es una petición HTMX? Devolver solo contenido parcial
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/expense_list_content.html', context)
    
    # Petición normal: devolver página completa
    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    """
    Vista refactorizada para agregar gastos - soporta modal HTMX
    Utiliza funciones auxiliares para mantener el código limpio y organizado
    """
    if request.method == 'POST':
        # Manejar creación del gasto usando función auxiliar
        expense, form, is_valid = handle_expense_creation(request.POST, request.user)
        
        # Formulario válido: respuesta HTMX con mensaje de éxito
        if is_valid and request.headers.get('HX-Request'):
            return create_htmx_add_response(request, expense)
        
        # Formulario válido: redirect normal
        if is_valid:
            messages.success(request, '¡Gasto agregado exitosamente!')
            return redirect('expenses:dashboard')
        
        # Formulario con errores: mostrar modal HTMX
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/add_expense_modal.html', {
                'form': form
            })
    
    else:
        # Obtener contexto usando función auxiliar
        context = build_add_expense_context()
        
        # Mostrar formulario: modal HTMX o página completa
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/add_expense_modal.html', context)
        
        return render(request, 'expenses/add_expense.html', context)


@login_required
def close_modal(request):
    """
    Vista para cerrar modales HTMX
    """
    return render(request, 'expenses/partials/empty.html')


@login_required
def delete_expense(request, expense_id):
    """
    Vista refactorizada para eliminar un gasto con HTMX
    Utiliza funciones auxiliares para mantener el código limpio y organizado
    """
    if request.method == 'DELETE':
        # Manejar eliminación del gasto usando función auxiliar
        expense_data, is_deleted, error_message = handle_expense_deletion(expense_id, request.user)
        
        # Eliminación exitosa: respuesta HTMX con lista actualizada
        if is_deleted and request.headers.get('HX-Request'):
            context = build_delete_success_context(request.user, expense_data, request.GET)
            return create_htmx_delete_response(request, context)
        
        # Eliminación exitosa: redirect normal
        if is_deleted:
            messages.success(request, f'Gasto de €{expense_data["amount"]} eliminado exitosamente')
            return redirect('expenses:expense_list')
        
        # Error en eliminación: manejar respuesta de error
        return handle_expense_error_response(request, error_message)


@login_required
def edit_expense(request, expense_id):
    """
    Vista refactorizada para editar un gasto con HTMX
    Utiliza funciones auxiliares para mantener el código limpio y organizado
    """
    try:
        # Obtener el gasto usando función auxiliar
        expense = get_expense_for_user(expense_id, request.user)
        
        if request.method == 'POST':
            updated_expense, form, is_valid = handle_expense_form_update(expense, request.POST)
            
            # Formulario válido: respuesta HTMX con actualización de lista
            if is_valid and request.headers.get('HX-Request'):
                context = build_expense_edit_context(request.user, updated_expense, form, request.GET)
                return create_htmx_edit_response(request, context)
            
            # Formulario válido: redirect normal
            if is_valid:
                messages.success(request, f'Gasto de €{updated_expense.amount} actualizado exitosamente')
                return redirect('expenses:expense_list')
            
            # Formulario con errores: mostrar modal HTMX
            if request.headers.get('HX-Request'):
                return render(request, 'expenses/partials/edit_expense_modal.html', {
                    'form': form,
                    'expense': expense,
                    'form_errors': True
                })
            
        else:
            form = ExpenseForm(instance=expense)
            
        # Mostrar formulario: modal HTMX o página completa
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/edit_expense_modal.html', {
                'form': form,
                'expense': expense
            })
        
        return render(request, 'expenses/edit_expense.html', {
            'form': form,
            'expense': expense
        })
        
    except Expense.DoesNotExist:
        return handle_expense_error_response(
            request, 
            'El gasto no existe o no tienes permisos para editarlo'
        )



