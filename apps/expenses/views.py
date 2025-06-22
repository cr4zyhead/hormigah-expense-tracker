from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm
from .utils import get_dashboard_context, get_expense_list_context


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
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            # Si es petición HTMX, devolver respuesta especial
            if request.headers.get('HX-Request'):
                # Cerrar modal y mostrar mensaje de éxito
                return render(request, 'expenses/partials/expense_success.html', {
                    'expense': expense,
                    'message': '¡Gasto agregado exitosamente!'
                })
            
            # Petición normal: redirect tradicional
            messages.success(request, '¡Gasto agregado exitosamente!')
            return redirect('expenses:dashboard')
        else:
            # Si hay errores y es HTMX, devolver modal con errores
            if request.headers.get('HX-Request'):
                return render(request, 'expenses/partials/add_expense_modal.html', {
                    'form': form
                })
    else:
        form = ExpenseForm()
    
    # Si es petición HTMX, devolver modal
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/add_expense_modal.html', {
            'form': form
        })
    
    # Petición normal: página completa
    context = {
        'form': form,
    }
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
    Vista para eliminar un gasto con HTMX
    """
    try:
        # Obtener el gasto y verificar que pertenece al usuario
        expense = Expense.objects.get(id=expense_id, user=request.user)
        
        if request.method == 'DELETE':
            # Guardar datos para el mensaje de confirmación
            expense_data = {
                'amount': expense.amount,
                'category_name': expense.category.name,
                'description': expense.description or 'Sin descripción',
                'date': expense.date
            }
            
            # Eliminar el gasto
            expense.delete()
            
            # Si es petición HTMX, devolver lista actualizada con mensaje
            if request.headers.get('HX-Request'):
                # Obtener contexto actualizado para la lista
                context = get_expense_list_context(request.user, request.GET)
                context.update({
                    'delete_success': True,
                    'expense_data': expense_data,
                    'delete_message': 'Gasto eliminado exitosamente'
                })
                return render(request, 'expenses/partials/expense_list_content.html', context)
            
            # Petición normal: redirect con mensaje
            messages.success(request, f'Gasto de €{expense_data["amount"]} eliminado exitosamente')
            return redirect('expenses:expense_list')
            
    except Expense.DoesNotExist:
        # El gasto no existe o no pertenece al usuario
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/delete_error.html', {
                'error': 'El gasto no existe o no tienes permisos para eliminarlo'
            })
        
        messages.error(request, 'El gasto no existe o no tienes permisos para eliminarlo')
        return redirect('expenses:expense_list')


@login_required
def edit_expense(request, expense_id):
    """
    Vista para editar un gasto con HTMX
    """
    try:
        # Obtener el gasto y verificar que pertenece al usuario
        expense = Expense.objects.get(id=expense_id, user=request.user)
        
        if request.method == 'POST':
            # Procesar formulario de edición
            form = ExpenseForm(request.POST, instance=expense)
            if form.is_valid():
                # Guardar cambios
                updated_expense = form.save()
                
                # Si es petición HTMX, devolver lista actualizada con mensaje
                if request.headers.get('HX-Request'):
                    context = get_expense_list_context(request.user, request.GET)
                    context.update({
                        'edit_success': True,
                        'expense_data': {
                            'amount': updated_expense.amount,
                            'category_name': updated_expense.category.name,
                            'description': updated_expense.description or 'Sin descripción',
                            'date': updated_expense.date
                        },
                        'edit_message': 'Gasto actualizado exitosamente'
                    })
                    
                    # Crear respuesta que actualiza la lista y cierra el modal
                    response = render(request, 'expenses/partials/expense_list_content.html', context)
                    # Usar HX-Trigger para cerrar el modal después de actualizar
                    response['HX-Trigger-After-Swap'] = 'closeEditModal'
                    return response
                
                # Petición normal: redirect con mensaje
                messages.success(request, f'Gasto de €{updated_expense.amount} actualizado exitosamente')
                return redirect('expenses:expense_list')
            else:
                # Formulario con errores
                if request.headers.get('HX-Request'):
                    return render(request, 'expenses/partials/edit_expense_modal.html', {
                        'form': form,
                        'expense': expense,
                        'form_errors': True
                    })
        else:
            # GET: Mostrar formulario de edición
            form = ExpenseForm(instance=expense)
            
        # Si es petición HTMX, devolver modal de edición
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/edit_expense_modal.html', {
                'form': form,
                'expense': expense
            })
        
        # Petición normal: renderizar página completa
        return render(request, 'expenses/edit_expense.html', {
            'form': form,
            'expense': expense
        })
        
    except Expense.DoesNotExist:
        # El gasto no existe o no pertenece al usuario
        if request.headers.get('HX-Request'):
            return render(request, 'expenses/partials/delete_error.html', {
                'error': 'El gasto no existe o no tienes permisos para editarlo'
            })
        
        messages.error(request, 'El gasto no existe o no tienes permisos para editarlo')
        return redirect('expenses:expense_list')



