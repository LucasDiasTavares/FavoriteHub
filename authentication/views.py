from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from utils.renderers import UserRender
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response({
            'tokens': {
                'access': data.tokens()['access'],
                'refresh': data.tokens()['refresh']
            },
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
