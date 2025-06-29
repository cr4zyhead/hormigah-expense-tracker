from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario
    Permite modificar email, nombre y apellidos para configuración de alertas n8n
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Tu apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'tu@email.com',
                'required': True
            }),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        help_texts = {
            'email': 'Este email se usará para las alertas y reportes automáticos de n8n',
            'first_name': 'Opcional - para personalizar los reportes',
            'last_name': 'Opcional - para personalizar los reportes'
        }
    
    def clean_email(self):
        """
        Validación personalizada para el email
        """
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que no exista otro usuario con este email (excepto el actual)
            existing_user = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise forms.ValidationError('Ya existe otro usuario con este email.')
        return email 