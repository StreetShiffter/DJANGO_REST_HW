import stripe
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from educations.models import Course, Lesson
from educations.serializers import CourseSerializer, LessonSerializer
from users.models import Payment, User, Subscription
from users.serializers import PaymentSerializer, UserSerializer, UserProfileSerializer
from users.services import create_stripe_product_and_price, process_lesson_payment, process_course_payment


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
    """Вьюшка для показа списков пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


class UserProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserSubscribeAPIView(APIView):
    """API для управления подпиской пользователя на курс: подписаться/отписаться
    работает только с теми методами, которые переопределены"""
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        user = request.user
        # Лучше передавать data в body, а не в GET(используется при POST, PUT, PATCH с форматами: JSON, form-data, etc.)
        # Передача числа курса в теле запроса(request - тело словарь(data), course_id - ключ)
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать 'course_id' в теле запроса."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            return Response(
                {"error": "Некорректный ID курса."},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли уже подписка
        subscription = Subscription.objects.filter(user=user, course=course).first()

        if subscription:
            if subscription.is_active:
                subscription.deactivate()
                message = "Подписка деактивирована"
            else:
                subscription.activate()
                message = "Подписка активирована"
        else:
            Subscription.objects.create(user=user, course=course, is_active=True)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class PayCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, *args, **kwargs):
        try:
            result = process_course_payment(request.user, course_id)
            course_data = CourseSerializer(result["course"], context={'request': request}).data
            return Response({
                "checkout_url": result["checkout_url"],
                "course": course_data,
                "payment_id": result["payment"].id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PayLessonAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id, *args, **kwargs):
        try:
            result = process_lesson_payment(request.user, lesson_id)
            lesson_data = LessonSerializer(result["lesson"], context={'request': request}).data
            return Response({
                "checkout_url": result["checkout_url"],
                "lesson": lesson_data,
                "payment_id": result["payment"].id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )