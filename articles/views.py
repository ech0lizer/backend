from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer, ArticleCreateSerializer
from .models import Article


class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleCreateAPIView(CreateAPIView):
    serializer_class = ArticleCreateSerializer
    queryset = Article.objects.all()


class ArticlesOptions(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
