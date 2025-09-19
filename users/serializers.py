from rest_framework.serializers import ModelSerializer
from users.models import Payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор модели 'Платежи'"""

    class Meta:
        model = Payment
        fields = "__all__"
