from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango
from apps.user.forms import RegisterForm, LoginForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

class UserProfileView(TemplateView):
    template_name = 'users/user_profile.html'

class RegisterView(CreateView):
    template_name = 'auth/auth_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home') # Redirige al home una vez registrado

    def form_valid(self, form):
        # Llama a la función form_valid de la clase padre y guarda el usuario
        response = super().form_valid(form)

        # Asignar el grupo Registered al usuario recién creado
        registered_group = Group.objects.get(name='Registered')
        self.object.groups.add(registered_group)

        # En caso de ser necesario se le puede asignar explicitamente los permisos del grupo al usuario
        # for permission in registered_group.permissions.all():
        # self.object.user_permissions.add(permission)
        return response
    
class LoginView(LoginViewDjango):
    template_name = 'auth/auth_login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')
    
class LogoutView(LogoutViewDjango):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')
    

