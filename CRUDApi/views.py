from django.shortcuts import render
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
# FOR GENERIC VIEWS
from rest_framework import generics
from rest_framework import mixins
# SETTING UP AUTHENTICATION SCHEME
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# class for GenericAPIViews
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    # used for put method
    lookup_field = 'id'

    # SETTING UP AUTHENTICATION
    # authentication_classes = [SessionAuthentication, BasicAuthentication] #for basic authentication
    authentication_classes = [TokenAuthentication] 
    
    permission_classes = [IsAuthenticated]
    
    # the methods require less code as compared to the ones using apiview

    # get method has a condition. first check whether url has been provided in the url. if yes, we use the retrieve model. If no, we use the list model

    def get(self, request, id= None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request) #Using listmodel mixin

    def post(self, request):
        return self.create(request)  #using createModel mixin

    def put(self, request, id=None):
        return self.update(request, id) # using updateModelMixin

    def delete(self, request, id):
        return self.destroy(request, id)



class ArticleAPIView (APIView): #this class extends from APIVIEW

    def get(self, request):
        articles = Article.objects.all()
        # serialize. We add many=true because this is a query set, we are fetching more than one article.
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data = request.data)

        # check whether data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            return HttpResponse (status = status.HTTP_404_NOT_FOUND)

        
    def get (self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)

        # check whether data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)