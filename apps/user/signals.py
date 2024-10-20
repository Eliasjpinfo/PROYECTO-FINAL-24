from django.db.models.signals import post_save
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from apps.user.models import User
from apps.post.models import Post, Comment

@receiver(post_save, sender=User)
def create_groups_and_permissions(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        try:
            post_content_type = ContentType.objects.get_for_model(Post)
            comment_content_type = ContentType.objects.get_for_model(Comment)

            # Permisos POST
            view_post_permission = Permission.objects.get(
                codename="view_post", content_type=post_content_type)
            add_post_permission = Permission.objects.get(
                codename="add_post", content_type=post_content_type)
            change_post_permission = Permission.objects.get(
                codename="change_post", content_type=post_content_type)
            delete_post_permission = Permission.objects.get(
                codename="delete_post", content_type=post_content_type)

            # Permisos COMMENTARIOS
            view_comment_permission = Permission.objects.get(
                codename="view_comment", content_type=comment_content_type)
            add_comment_permission = Permission.objects.get(
                codename="add_comment", content_type=comment_content_type)
            change_comment_permission = Permission.objects.get(
                codename="change_comment", content_type=comment_content_type)
            delete_comment_permission = Permission.objects.get(
                codename="delete_comment", content_type=comment_content_type)

            # CREAR GRUPO USUARIOS REGISTRADOS
            registered_group, created = Group.objects.get_or_create(
                name='Registered')
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
            )

            # CREAR GRUPO USUARIOS COLABORADORES
            registered_group, created = Group.objects.get_or_create(
                name='Collaborators')
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
            )   

            #CREAR GRUPO USUARIOS ADMINISTRADORES(HEAVY)
            registered_group, created = Group.objects.get_or_create(
                name='Admins')
            registered_group.permissions.set(Permission.objects.all())
            
            print("Se crearon los grupos y permisos")
        
        except ContentType.DoesNotExist:
            print('El tipo de contenido aun no esta disponible.')
        except Permission.DoesNotExist:
            print('Uno o mas permisos no estan disponible aun.')