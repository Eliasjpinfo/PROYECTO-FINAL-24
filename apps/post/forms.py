from django import forms
from apps.post.models import Post, PostImage, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'allow_comments')

class NewPostForm(PostForm):
    image = forms.ImageField(required=False)

    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data['image']

        if commit:
            post.save()
            if self.cleaned_data['image']:
                PostImage.objects.create(post=post, image=self.cleaned_data['image'])
        return post

class UpdatePostForm(PostForm):
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        # Obtenemos las imágenes activas del post que se quiere actualizar
        self.active_images = kwargs.pop('active_images', None)
        super(UpdatePostForm, self).__init__(*args, **kwargs)

        if self.active_images:
            for image in self.active_images:
                # keep_image_1, keep_image_2, ... etc es el nombre del campo que se creará en el formulario para mantener la imagen activa
                field_name = f"keep_image_{image.id}"
                self.fields[field_name] = forms.BooleanField(
                    required=False, initial=True, label=f"Mantener {image}"
                )

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            if self.cleaned_data['image']: # Si el usuario sube una nueva imagen
                PostImage.objects.create(
                    post=post, image=self.cleaned_data['image'])

            if self.active_images: # Si hay imágenes activas y se quiere mantener alguna
                for image in self.active_images:
                    if not self.cleaned_data.get(f"keep_image_{image.id}", True):
                        image.delete() # Eliminar la imagen si el usuario no la quiere mantener, checkboxes desmarcados
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content': 'Comentario'
        }

        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario...', 'class': 'p-2'})
        }

class PostFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Buscar...', 'class': 'w-full p-2'})
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=(
            ('-creation_date', 'Más reciente'),
            ('creation_date', 'Más antiguo'),
            ('-comments_count', 'Más comentado'),
        ),
        widget=forms.Select(attrs={'class': 'w-full p-2'})
    )