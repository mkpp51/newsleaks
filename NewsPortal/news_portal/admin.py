from django.contrib import admin
from .models import Post, Author, Category, Comment


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post_header', 'post_auth', 'post_pub_date')
    list_filter = ('post_cat', 'post_auth')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('post_header', 'post_auth', 'post_cat')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
