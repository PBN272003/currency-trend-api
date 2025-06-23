from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer
    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=CustomUserSerializer,
        responses={201: CustomUserSerializer, 400: "Invalid data"}
    )
    def post(self, request, *args, **kwargs):
        """Handle user registration"""
        return super().post(request, *args, **kwargs)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
    
    @swagger_auto_schema(
        operation_description="Retrieve logged-in user's profile.",
        responses={200: CustomUserSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update logged-in user's profile.",
        request_body=CustomUserSerializer,
        responses={200: CustomUserSerializer, 400: "Invalid data"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update logged-in user's profile.",
        request_body=CustomUserSerializer,
        responses={200: CustomUserSerializer, 400: "Invalid data"}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
