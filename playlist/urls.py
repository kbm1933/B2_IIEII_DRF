from django.urls import path
from playlist import views

urlpatterns = [
    # 게시글 => GET : 게사글 다 불러오고 / POST : 게시글을 작성 할 수 있게끔 하는 페이지
    path('<int:list_id>/', views.CustomPlaylistView.as_view(), name='playlist_view'),
    path('<int:list_id>/<int:user_id>/', views.CustomPlaylistDetailView.as_view(), name='playlist_detail_view'),
]