from django.contrib.auth.models import User, AbstractUser
from django.db import models
from tinymce.models import HTMLField
from PIL import Image

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

class Post(models.Model):
    title = models.CharField()
    content = HTMLField()
    author = models.ForeignKey(to='blog.CustomUser', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='post_photos', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to="Post",
                             on_delete=models.CASCADE,
                             related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(to='blog.CustomUser', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f"{self.author} ({self.date_created})"
