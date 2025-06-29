from django import forms
from django.contrib.auth.models import User
from apps.expenses.models import Budget


class UserProfileForm(forms.ModelForm):
    """
    Formulario para editar el perfil del usuario
    Permite modificar email, nombre y apellidos para configuración de alertas n8n
    """
    
    # Campo adicional para alertas por email (del modelo Budget)
    email_alerts_enabled = forms.BooleanField(
        required=False,
        label="Alertas por Email",
        help_text="Recibir notificación por email al superar el límite de presupuesto",
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
    )
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar el campo de alertas si el usuario tiene presupuesto
        if self.instance and hasattr(self.instance, 'budget'):
            self.fields['email_alerts_enabled'].initial = self.instance.budget.email_alerts_enabled
        else:
            # Si no tiene presupuesto, no mostrar el campo
            del self.fields['email_alerts_enabled']
    
    def save(self, commit=True):
        """
        Guardar tanto el usuario como la configuración de alertas del presupuesto
        """
        user = super().save(commit=commit)
        
        # Si el campo de alertas existe y el usuario tiene presupuesto
        if 'email_alerts_enabled' in self.cleaned_data and hasattr(user, 'budget'):
            user.budget.email_alerts_enabled = self.cleaned_data['email_alerts_enabled']
            if commit:
                user.budget.save()
        
        return user
    
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