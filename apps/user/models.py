# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import uuid

def get_avatar_filename(instance, filename):
    base_filename, file_extension = os.path.splittext(filename)
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    return os.path.join('user/avatar/', new_filename)


class User(AbstractUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(
        upload_to=get_avatar_filename, default='user/default/avatar_default.jpg')

    @property
    def is_collaborator(self):
        return self.groups.filter(name='Collaborators').exists()
    
    @property
    def is_admin(self):
        return self.groups.filter(name='Admins').exists()
    
    @property
    def is_registered(self):
        return self.groups.filter(name='Registered').exists()