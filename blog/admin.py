from django.contrib import admin

# Register your models here.

from  .models import Post, User,Category,Comment

#admin.site.register(Post)

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'title', 'author')
    list_filter = ('title_id', 'title', 'author')
    search_fields = ('title_id', 'title', 'author')
    ordering= ('title_id', 'title', 'author')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','first_name')

admin.site.register(Category)
admin.site.register(Comment)