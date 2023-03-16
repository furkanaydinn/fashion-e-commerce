from django.contrib import admin
from .models import Blog, Comment


# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]
    list_display = ('title', 'author_name', 'status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)