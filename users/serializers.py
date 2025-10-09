from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from users.models import Payment, User, Subscription


class SubscribeSerializer(ModelSerializer):
    """Сериализатор модели 'Подписки'"""

    class Meta:
        model = Subscription
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    """Сериализатор модели 'Платежи'"""

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "course",
            "lesson",
            "amount",
            "payment_method",
            "payment_date",
            "stripe_session_id",
        ]
        read_only_fields = ["id", "user", "payment_date"]


class UserSerializer(ModelSerializer):
    """Сериализатор редактирования"""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True}  # чтобы пароль не возвращался в ответе
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileSerializer(ModelSerializer):
    """Сериализатор просмотр профиля"""

    subscribe = SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "subscribe"]
        read_only_fields = fields  # Только для чтения
