"""
URL configuration for videosubscription project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from User.views import LoginView, SignUpView
from subscription.views import SubscriptionViewSet, MockPaymentViewSet 
from rest_framework.routers import DefaultRouter 
from Video.views import MovieViewSet, ReviewViewSet, WatchlistViewSet, MovieListView
from Video.views import CastListView, CastAdminViewSet, GenreListView, GenreAdminViewSet
from User.views import UpdateProfileViewSet, ChangePasswordView


router = DefaultRouter()  
router.register(r'subscription', SubscriptionViewSet, basename='subscription')  
router.register(r'movies', MovieViewSet, basename='movies')  
router.register(r'reviews', ReviewViewSet, basename='review')  
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'movies-list', MovieListView, basename='movies-list')  
router.register(r'profile', UpdateProfileViewSet, basename='profile') 
router.register(r'casts', CastListView, basename='casts')   
router.register(r'createcasts', CastAdminViewSet, basename='createcast')   
router.register(r'genres', GenreListView, basename='genres')  
router.register(r'creategenres', GenreAdminViewSet, basename='creategenres') 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mock-payment/', MockPaymentViewSet.as_view({'post': 'create'}), name='mock-payment'),  
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('api/', include(router.urls)), 
    path('api/change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
]
