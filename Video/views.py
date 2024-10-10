from rest_framework import viewsets  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser  
from .models import Movie, Review, Watchlist, CustomUser, Cast
from .serializers import MovieSerializer, ReviewSerializer, WatchlistSerializer, CastSerializer
from django.http import FileResponse, Http404

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

class CastListView(viewsets.ReadOnlyModelViewSet):  
    queryset = Cast.objects.all()  
    serializer_class = CastSerializer 
    permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):  
    serializer_class = ReviewSerializer  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):  
    
        return Review.objects.filter(user=self.request.user)  

    def perform_create(self, serializer):  
        
        serializer.save(user=self.request.user)   

class VideoStreamView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request, movie_id):  
        try:  
            movie = Movie.objects.get(id=movie_id)  
            movie.view += 1   
            movie.save()
            response = FileResponse(open(movie.video_file.path, 'rb'), content_type='video/mp4')  
            return response  
        except Movie.DoesNotExist:  
            raise Http404("Movie not found.")  
        except FileNotFoundError:  
            raise Http404("Video file not found.")  

class VideoDownloadView(APIView):
    permission_classes = [IsAuthenticated]   
    def get(self, request, movie_id):  
        try:  
            movie = Movie.objects.get(id=movie_id)  
            movie.view += 1   
            movie.save()
            file_handle = open(movie.video_file.path, 'rb')  
            response = FileResponse(file_handle, as_attachment=True, content_type='video/mp4')  
            response['Content-Disposition'] = f'attachment; filename="{movie.title}.mp4"'
            response = FileResponse(open(movie.video_file.path, 'rb'), as_attachment=True, content_type='application/octet-stream')  
            return response  
        except Movie.DoesNotExist:  
            raise Http404("Movie not found.")  
        except FileNotFoundError:  
            raise Http404("Video file not found.")                   