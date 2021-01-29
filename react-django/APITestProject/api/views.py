from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, UserSerializer
from .models import Article
from django.contrib.auth.models import User

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

class UserViweSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

