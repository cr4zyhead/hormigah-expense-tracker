from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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



