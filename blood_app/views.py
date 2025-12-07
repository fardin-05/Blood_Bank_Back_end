from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BloodRequest, DonationHistory
from .serializers import BloodRequestSerializer, DonationHistorySerializer

class MyRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        my_request = BloodRequest.objects.filter(created_by=request.user)
        serializer = BloodRequestSerializer(my_request, many=True)

        return Response({
            "message":"Your Created Blood Requests",
            "count":my_request.count(),
            "data":serializer.data
        },status=status.HTTP_200_OK)


class IncomingRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_group = request.user.blood_group
        incoming = BloodRequest.objects.filter(blood_group_needed=my_group, status="Panding").exclude(created_by=request.user)
        serializer = BloodRequestSerializer(incoming, many=True)

        return Response({
            "message":"Incoming Request You can accept",
            "count": incoming.count(),
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    

class MyDonationHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = DonationHistory.objects.filter(donor=request.user) | DonationHistory.objects.filter(receiver=request.user)
        serializer = DonationHistorySerializer(history, many=True)

        return Response({
            "message":"Your Donation History",
            "count":history.count(),
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    

class AllBloodRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = BloodRequest.objects.exclude(created_by=request.user)
        serializer = BloodRequestSerializer(requests, many=True)
        return Response(
            {
                "message":"All blood request(eexcluding your ownn)",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class CreateBloodRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BloodRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {
                    "message":"Blood request created successfully",
                    "data":serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AcceptBloodRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            blood_request = BloodRequest.objects.get(id=pk)
        except BloodRequest.DoesNotExist:
            return Response(
                {
                    "error":"Blood request not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if blood_request.created_by == request.user:
            return Response(
                {
                    "error":"You cannot accept your own request"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if blood_request.status == 'ACCEPTED':
            return Response(
                {
                    "error":"This request is already accepted"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        blood_request.status = "ACCEPTED"
        blood_request.accepted_by = request.user
        blood_request.save()

        DonationHistory.objects.create(
            donor=request.user,
            receiver=blood_request.created_by,
            event=blood_request,
            status="PENDING"
        )
        return Response(
            {
                "message":"Request accepted successfully",
                "data":BloodRequestSerializer(blood_request).data
            },
            status=status.HTTP_200_OK
        )
  