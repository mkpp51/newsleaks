from django.urls import path
from . import views

from .views import PostList, PostDetail, NewsCreate, ProtectedNewsEdit, NewsDelete, ArticlesCreate, \
   ProtectedArticlesEdit, ArticlesDelete, PostSearch, add_subscriber

from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(PostList.as_view())),
   path('<int:pk>', cache_page(60 * 5)(PostDetail.as_view()), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', ProtectedNewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ProtectedArticlesEdit.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='Articles_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('categories/', views.all_categories, name='categories'),
   path('categories/<str:category>', views.category, name='category'),
   path('categories/<str:category>/add_subscriber/', add_subscriber, name='add_subscriber'),
   ]
