from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, Comment, CustomUser

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created']
    list_filter = ['author', 'date_created']
    search_fields = ['title', 'content']
    inlines = [CommentInLine]


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {'fields': ['photo']}),
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(CustomUser, CustomUserAdmin)
