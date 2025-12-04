from django.urls import path
from .views import( 
    UserListAPIView, 
    UserDetailAPIView, 
    UserProfileUpdateAPIView,
    PublicDonorListAPIView,
    
    )
urlpatterns = [
    path('',UserListAPIView.as_view(), name='user_list'),
    path('<int:id>/', UserDetailAPIView.as_view()),
    path('profile/update/',UserProfileUpdateAPIView.as_view()),
    path('donors/',PublicDonorListAPIView.as_view()),
   
    
]
