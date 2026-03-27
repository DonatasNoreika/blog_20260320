from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField

class Post(models.Model):
    title = models.CharField()
    content = HTMLField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='post_photos', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(to="Post",
                             on_delete=models.CASCADE,
                             related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f"{self.author} ({self.date_created})"
