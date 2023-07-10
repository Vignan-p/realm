# urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import player_view, movie_upload

urlpatterns = [
    path('',views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('profiles/', views.profile, name='profiles'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('profiles/<int:profile_id>/edit/', views.edit_profile, name='edit_profile'),
    path('profiles/<int:profile_id>/delete/', views.delete_profile, name='delete_profile'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('movie_upload',movie_upload, name='movie_upload'),
    path('signup', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('videos/<int:genre_id>/',views.video_list, name='video_list'),
    path('player/', player_view, name='player'),
    path('search/', views.search, name='search'),
    path('search_kids/', views.search_kids, name='search_kids'),
    path('schedule',views.schedule,name='schedule'),
    path('home_kids/', views.home_kids, name='home_kids'),
    path('video_list1/<int:genre_id>/', views.video_list1, name='video_list1'),
    path('player/<int:video_id>/', views.player, name='player'),
    path('unlock-pin', views.unlock_pin, name='unlock_pin'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)