from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BloodRequest, DonationHistory
from .serializers import BloodRequestSerializer


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
  