from django.contrib import admin
from .models import Blog,BlogComment,BlogCategory
# Register your models here.

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','author','pub_time','category','content']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['content','author','pub_time','blog']


admin.site.register(BlogCategory,BlogCategoryAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogComment,BlogCommentAdmin)