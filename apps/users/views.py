from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from apps.users.models import User, Kura
from apps.users.serializers import UserSerializer, UserRegisterSerializer, KuraSerializers

class UserAPI(GenericViewSet,
              mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegisterAPI(GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Ошибки валидации:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "Пользователь успешно зарегистрирован"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class KuraAPI(GenericViewSet,
              mixins.CreateModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin):
    queryset = Kura.objects.all()
    serializer_class = KuraSerializers
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

def register(request):
    return render(request, 'sign_up.html', locals())

def login(request):
    return render(request, 'login.html', locals())

def kura_user(request):
    return render(request, 'become_courier.html', locals())