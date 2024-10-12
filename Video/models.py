from django.db import models
from User.models import CustomUser


class Genres(models.Model):
    name = models.CharField(max_length=50)
    detail = models.TextField(default="")

    def __str__(self):
        return self.name

class Cast(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    biography = models.TextField(default="")
    image = models.FileField(upload_to='cast/', max_length=600, null=True, blank=True) 

    def __str__(self):
        return self.name  


class Movie(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default="")
    url = models.URLField(max_length=600, blank=True, null=True)
    upload_date = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    genres = models.ManyToManyField(Genres)
    cast = models.ManyToManyField(Cast)
    poster = models.FileField(upload_to = 'movie/poster/', max_length=600, null=True)
    view = models.IntegerField(default=0)


class Watchlist(models.Model):
    '''
    It will contain the movies and series that a user will add to his watchlist
    '''
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    
    class Meta:  
        unique_together = ('user', 'movie')


class Review(models.Model): 
    CHOICES = {
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    }
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(choices=CHOICES)
    comment = models.TextField(null=True, blank=True)
    
