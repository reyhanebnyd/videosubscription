from rest_framework import serializers  
from .models import Movie, Review, Watchlist, Cast , Genres

class MovieSerializer(serializers.ModelSerializer):  
    genres = serializers.SerializerMethodField()  
    cast = serializers.SerializerMethodField()

    class Meta:  
        model = Movie  
        fields = '__all__'  

    
    def get_genres(self, obj):  
        return [genre.name for genre in obj.genres.all()]  

    def get_cast(self, obj):  
        return [cast.name for cast in obj.cast.all()]      

class ReviewSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Review  
        fields = '__all__' 
        extra_kwargs = {
            'user': {'read_only': True},
        } 

class WatchlistSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Watchlist  
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        } 

class CastSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Cast  
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Genres 
        fields = '__all__'
