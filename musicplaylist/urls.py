from django.urls import path
from musicplaylist import views

urlpatterns = [
    # 1. API 선호하는 음악선택
    path('<int:user_id>/playlist/select/', views.PlayListUserSelect.as_view(), name='musicplaylistuserselect_view'),
    
    # 2. API 추천 플레이 리스트
    path('<int:user_id>/playlist/recommended/', views.PlayListRecommended.as_view(), name='musicplaylistuserrecommnded_view'),

    # 3. API 유저커스텀 플레이 리스트
    path('<int:user_id>/', views.PlayListview.as_view(), name='playlist_view'),
    
    # 4. API 유저커스텀 플레이 리스트 상세
    path('<int:playlist_id>/detail/', views.PlayListDetailview.as_view(), name='playlist_detail_view'),

]
