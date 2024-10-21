from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import os
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)

    def str(self):
        return self.title

from django.db import models

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title= models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    content = RichTextField(max_length=10000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    modification_date = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    

    def __str__(self):
        return self.title
    
    @property
    def amount_comments(self):
        return self.comments.count() #definir!!!
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

        #DEFINIR IMAGENES PORTADA

    def generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1

        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1

        return unique_slug

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content
    
def get_image_filename(instance, filename):
    post_id = instance.post.id
    images_count = instance.post.images.count()
    base_filename, file_extension = os.path.splitext(filename) # esto se llama unpacking (desempaquetado)
    new_filename = f"post_{post_id}_cover_{images_count + 1}{file_extension}"
    return os.path.join('post/cover/', new_filename)

class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_filename, default='post/default/post_default.png')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"PostImage {self.id}"
    
def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

        if not self.images.exists():
            PostImage.objects.create(post=self, image='post/default/post_default.png')




