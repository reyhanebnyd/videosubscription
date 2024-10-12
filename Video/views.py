from rest_framework import viewsets  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser  
from .models import Movie, Review, Watchlist, CustomUser, Cast, Genres
from .serializers import MovieSerializer, ReviewSerializer, WatchlistSerializer, CastSerializer, GenreSerializer
from django.http import FileResponse, Http404
from django.db.models import Avg  
from channels.layers import get_channel_layer  
from asgiref.sync import async_to_sync  
from rest_framework.response import Response

class MovieViewSet(viewsets.ModelViewSet):  
    queryset = Movie.objects.all()  
    serializer_class = MovieSerializer  
    permission_classes = [IsAdminUser]  

class ReviewViewSet(viewsets.ModelViewSet):  
    queryset = Review.objects.all()  
    serializer_class = ReviewSerializer  
    permission_classes = [IsAuthenticated]    

class WatchlistViewSet(viewsets.ModelViewSet):    
    serializer_class = WatchlistSerializer  
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):  
     
        serializer.save(user=self.request.user)  

    def get_queryset(self):  
        
        return Watchlist.objects.filter(user=self.request.user)

class MovieListView(viewsets.ReadOnlyModelViewSet):  
    queryset = Movie.objects.all()  
    serializer_class = MovieSerializer  
    permission_classes = [IsAuthenticated]  
    

    def retrieve(self, request, *args, **kwargs):  
        
        instance = self.get_object()  

         
        instance.view += 1  
        instance.save()   
        

         
        average_rating = Review.objects.filter(movie=instance).aggregate(Avg('rating'))['rating__avg']  
        comments = Review.objects.filter(movie=instance).values('comment')  

         
        serializer = self.get_serializer(instance)  
        response_data = serializer.data  
        response_data['average_rating'] = average_rating  
        response_data['comments'] = list(comments)   

        channel_layer = get_channel_layer()  
        async_to_sync(channel_layer.group_send)(  
            f'movie_{instance.id}',    
            {  
                'type': 'send_update',  
                'views': instance.view,  
                'average_rating': average_rating,  
                'comments': list(comments),  
            }  
        )  
        return Response(response_data)      

class ReviewViewSet(viewsets.ModelViewSet):  
    serializer_class = ReviewSerializer  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):  
    
        return Review.objects.filter(user=self.request.user)  

    def perform_create(self, serializer):  
        
        serializer.save(user=self.request.user) 
 

class CastAdminViewSet(viewsets.ModelViewSet):  
    queryset = Cast.objects.all()  
    serializer_class = CastSerializer  
    permission_classes = [IsAdminUser]   


class CastListView(viewsets.ReadOnlyModelViewSet):  
    queryset = Cast.objects.all()  
    serializer_class = CastSerializer  
    permission_classes = [IsAuthenticated]  

  
class GenreAdminViewSet(viewsets.ModelViewSet):  
    queryset = Genres.objects.all()  
    serializer_class = GenreSerializer  
    permission_classes = [IsAdminUser]  

  
class GenreListView(viewsets.ReadOnlyModelViewSet):  
    queryset = Genres.objects.all()  
    serializer_class = GenreSerializer  
    permission_classes = [IsAuthenticated]