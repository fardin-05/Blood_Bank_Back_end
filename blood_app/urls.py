from django.urls import path
from .views import( 
MyRequestAPIView,
IncomingRequestAPIView,
MyDonationHistoryAPIView,
CreateBloodRequestAPIView, 
AllBloodRequestAPIView, 
AcceptBloodRequestAPIView

)

urlpatterns = [
    path('my-request/',MyRequestAPIView.as_view(), name='my-requests'),
    path('incoming-request',IncomingRequestAPIView.as_view(), name='incoming-requests'),
    path('my-history',MyDonationHistoryAPIView.as_view(), name='my-history'),
    path('blood-request/create/',CreateBloodRequestAPIView.as_view()),
    path('blood-request/all/', AllBloodRequestAPIView.as_view()),
    path('blood-request/accept/<int:pk>/', AcceptBloodRequestAPIView.as_view()),


]
