from django.urls import path
from .views import ArticleAPIView, ArticleDetails, GenericAPIView

urlpatterns = [
    path('article/', ArticleAPIView.as_view()), # because this is a class, we have to include .as_view()
    path('detail/<int:id>/', ArticleDetails.as_view()),
    path('generic/article/', GenericAPIView.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view())
]

