from django.urls import path
from .views import CreateBloodRequestAPIView, AllBloodRequestAPIView, AcceptBloodRequestAPIView

urlpatterns = [
    path('blood-request/create/',CreateBloodRequestAPIView.as_view()),
    path('blood-request/all/', AllBloodRequestAPIView.as_view()),
    path('blood-request/accept/<int:pk>/', AcceptBloodRequestAPIView.as_view()),


]
