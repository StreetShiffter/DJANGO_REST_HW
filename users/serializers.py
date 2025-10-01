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
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True}  # чтобы пароль не возвращался в ответе
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class UserProfileSerializer(ModelSerializer):
    """Сериализатор просмотр профиля"""
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name",]
        read_only_fields = fields #Только для чтения


