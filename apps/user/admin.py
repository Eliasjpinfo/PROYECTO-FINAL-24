from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.user.models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        # None es el título del fieldset
        (None, {'fields': ('alias', 'avatar')}),
    ) # Campos en el formulario de edición de usuario

    add_fieldsets = (
        (None, {
        'fields': ('username', 'email', 'alias', 'avatar', 'password1', 'password2'),
        }),
    ) # Campos en el formulario de creación de usuario

    # Verificar si el usuario pertenece a un grupo específico
    def is_registered(self, obj):
        return obj.groups.filter(name='Registered').exists()
    is_registered.short_description = 'Es Usuario Registrado'
    is_registered.boolean = True

    def is_collaborator(self, obj):
        return obj.groups.filter(name='Collaborators').exists()
    is_collaborator.short_description = 'Es Colaborador'
    is_collaborator.boolean = True

    def is_admin(self, obj):
        return obj.groups.filter(name='Admins').exists()
    is_admin.short_description = 'Es Administrador'
    is_admin.boolean = True

    # Acciones de agregar usuarios a grupos
    def add_to_registered(self, request, queryset):
        registered_group = Group.objects.get(name='Registered')
        for user in queryset:
            user.groups.add(registered_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Registered'.")
    add_to_registered.short_description = 'Agregar a Usuarios Registrados'

    def add_to_collaborators(self, request, queryset):
        collaborators_group = Group.objects.get(name='Collaborators')
        for user in queryset:
            user.groups.add(collaborators_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Collaborators'.")
    add_to_collaborators.short_description = 'Agregar a Colaboradores'

    def add_to_admins(self, request, queryset):
        admins_group = Group.objects.get(name='Admins')
        for user in queryset:
            user.groups.add(admins_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Admins'.")
    add_to_admins.short_description = 'Agregar a Administradores'

    # Acciones de remover usuarios de grupos
    def remove_from_registered(self, request, queryset):
        registered_group = Group.objects.get(name='Registered')
        for user in queryset:
            user.groups.remove(registered_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Registered'.")
    remove_from_registered.short_description = 'Remover de Usuarios Registrados'

    def remove_from_collaborators(self, request, queryset):
        collaborators_group = Group.objects.get(name='Collaborators')
        for user in queryset:
            user.groups.remove(collaborators_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Collaborators'.")
    remove_from_collaborators.short_description = 'Remover de Colaboradores'

    def remove_from_admins(self, request, queryset):
        admins_group = Group.objects.get(name='Admins')
        for user in queryset:
            user.groups.remove(admins_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Admins'.")
    remove_from_admins.short_description = 'Remover de Administradores'

    # Agregar las acciones a la clase CustomUserAdmin
    actions = [add_to_registered, add_to_collaborators, add_to_admins, remove_from_registered,
        remove_from_collaborators, remove_from_admins]

    # Modificar el list_display para incluir los nuevos campos
    list_display = ('username', 'email', 'alias', 'is_staff', 'is_superuser', 'is_registered', 'is_collaborator', 'is_admin') # Campos a mostrar en la lista

    search_fields = ('username', 'email', 'alias', 'id') # Campos de búsqueda
    # Ordenar por fecha de creación mayor a menor(últimos primero)
    ordering = ('-date_joined',)


admin.site.register(User, CustomUserAdmin)
