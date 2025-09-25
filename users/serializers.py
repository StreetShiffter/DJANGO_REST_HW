from rest_framework.serializers import ModelSerializer
from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор модели 'Платежи'"""

    class Meta:
        model = Payment
        fields = "__all__"

class UserSerializer(ModelSerializer):
    """Сериализатор редактирования"""
    class Meta:
        model = User
        fields = "__all__"

class UserProfileSerializer(ModelSerializer):
    """Сериализатор просмотр профиля"""
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name",]
        read_only_fields = fields #Только для чтения


