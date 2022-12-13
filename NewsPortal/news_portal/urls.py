from django.urls import path

from .views import PostList, PostDetail, NewsCreate, NewsEdit, NewsDelete, ArticlesCreate, ArticlesEdit, \
   ArticlesDelete, PostSearch

urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='Articles_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   ]