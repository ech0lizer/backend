from django.urls import path
from .views import ArticleListAPIView, ArticlesOptions, ArticleCreateAPIView

urlpatterns = [
    path('', ArticleListAPIView.as_view(), name='articles-list'),
    path('create/', ArticleCreateAPIView.as_view(), name='article-create'),
    path('<int:id>', ArticlesOptions.as_view(), name='article-options')
]