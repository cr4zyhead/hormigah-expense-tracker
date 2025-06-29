from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

# Create your views here.

@login_required
def user_profile(request):
    """
    Vista para mostrar y editar el perfil del usuario
    Permite modificar nombre, apellido y email para configuración de alertas n8n
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'user': request.user
    })
