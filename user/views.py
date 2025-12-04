from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from djoser.utils import decode_uid
from .serializers import UserSerializer, UserProfileUpdateSerializer, DonorSerializer
from .models import CustomUser
class UserProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message":"Profile Updated Successfully",
                    "data":serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserListAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       #=========POST → Create new user============
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    #=========Helper: get user or return 404==========
    def get_user(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            raise CustomUser.DoesNotExist("User not found")
    def get(self, request, id):
        user = self.get_user(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

        
    #=========PUT → Full update by ID==========
    def put(self, request, id):
        user = self.get_user(id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully", "data": serializer.data},
                status=200
            )
        return Response(serializer.errors, status=400)

    #=========PATCH → Partial update by ID============
    def patch(self, request, id):
        user = self.get_user(id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User partially updated", "data": serializer.data},
                status=200
            )
        return Response(serializer.errors, status=400)

    #=========DELETE → delete user by ID==========
    def delete(self, request, id):
        user = self.get_user(id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)


#============Active User API When Activation Link Clicked=============
User = get_user_model()

class ActiveUserAPIView(APIView):
    def get(self, request, uid, token):
        try:
            uid = decode_uid(uid) #base64 decode
            user = User.objects.get(pk=uid)
        except(User.DoesNotExist, ValueError, TypeError):
            return Response({"error":"Invalid activation link"}, status=400)
        
    #=======Token Validity Check============
        
        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({"message":"Account activated successfully"}, status=200)
        else:
            return Response({"message":"Account already active"}, status=200)
        

class PublicDonorListAPIView(APIView):
    def get(self, request):
        blood_group = request.query_params.get("blood_group")
        donors = CustomUser.objects.filter(availability=True)

        if blood_group:
            donors = donors.filter(blood_group=blood_group)  
        serializer = DonorSerializer(donors, many=True)
        return Response(
            {
                "message":"Available Donor List",
                "count":donors.count(),
                "data":serializer.data
            }
        )
            