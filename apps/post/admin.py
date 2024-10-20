from django.contrib import admin
from apps.post.models import Post, Category, PostImage, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'creation_date', 'modification_date', 'allow_comments') # Campos a mostrar en la lista
    search_fields = ('title', 'content', 'author__username', 'id') # Campos de búsqueda
    prepopulated_fields = {'slug': ('title',)} # Autocompletar slug a partir del título
    list_filter = ('category', 'author', 'creation_date', 'allow_comments')
    ordering = ('-creation_date',) # Ordenar por fecha de creación descendente

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'creation_date')
    search_fields = ('content', 'author__username', 'post__title', 'id')
    list_filter = ('creation_date', 'author')
    ordering = ('-creation_date',) # Ordenar por fecha de creación descendente

def activate_images(modeladmin, request, queryset):
    updated = queryset.update(active=True)
    modeladmin.message_user(
        request, f"{updated} imágenes fueron activadas correctamente."
    )
activate_images.short_description = "Activar imágenes seleccionadas"

def deactivate_images(modeladmin, request, queryset):
    updated = queryset.update(active=False)
    modeladmin.message_user(
        request, f"{updated} imágenes fueron desactivadas correctamente."
    )
deactivate_images.short_description = "Desactivar imágenes seleccionadas"

class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'active') # Campos a mostrar en la lista
    # Buscar por título del post y nombre de la imagen
    search_fields = ('post__title', 'image')
    list_filter = ('active',) # Filtros en la lista
    # Agregar las acciones personalizadas
    actions = [activate_images, deactivate_images]

# Registrar los modelos en el admin
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostImage, PostImageAdmin)