from rest_framework import serializers  
from .models import Movie, Review, Watchlist, Cast 

class MovieSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Movie  
        fields = '__all__'  

class ReviewSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Review  
        fields = '__all__'  

class WatchlistSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Watchlist  
        fields = '__all__'

class CastSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Cast  
        fields = '__all__'        