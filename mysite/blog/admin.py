from django.contrib import admin

from .models import Post, Comment

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    list_filter = ['author', 'date_created']
    search_fields = ['title', 'content']
    inlines = [CommentInLine]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
