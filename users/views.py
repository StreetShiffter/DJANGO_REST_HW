from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserProfileSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюшка для ендпоинта фильтра и сортировки"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]

class UserCreateAPIview(CreateAPIView):
    """Вьюшка для создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Вьюшка для создания пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные

    def get_object(self):
        return self.request.user  # Всегда возвращает текущего пользователя

    def get_serializer_class(self):
        """Метод ловит действие 'retrieve', то перенаправляет на другой сериализатор"""
        if self.action == "retrieve":
            return UserProfileSerializer
        return UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

