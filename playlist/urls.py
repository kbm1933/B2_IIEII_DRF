from django.urls import path
from playlist import views

urlpatterns = [
    path('', views.PlayListview.as_view(), name='playlist_view'),
    path('musiclists/', views.MusicListview.as_view(), name='musiclist_view'),

    path('<int:article_id>/', views.PlayListDetailview.as_view(), name='playlist_detail_view'),

]