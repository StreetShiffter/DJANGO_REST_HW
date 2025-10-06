from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from educations.models import Course, Lesson
from educations.validators import CorrectVideoUrl, MatchVideoUrl
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    """Сериализатор модели 'Урок"""

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'preview', 'video_url', 'course', 'owner']
        validators = [CorrectVideoUrl(field = 'video_url'),
                      MatchVideoUrl(field = 'title'),
                      MatchVideoUrl(field = 'description')]


class CourseSerializerList(ModelSerializer):
    """Сериализатор модели 'Курс' для показа количества уроков"""
    is_subscribed = serializers.SerializerMethodField()

    count_lessons = SerializerMethodField()  # поля могут быть __all__
    # показ информации уроков в курсе(обязательно в перечислении полей
    # т.к.это внешний сериализатор[использовать related_name])
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # many = уроков может быть несколько(берем сериализатор урока)

    def get_count_lessons(self, obj):
        return (
            obj.lessons.count()
        )  # если в ForeginKey есть related_name - обращаемся по нему(или по obj_set)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj, is_active=True).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "count_lessons",
            "lessons",
            "is_subscribed"
        ]


class CourseSerializer(ModelSerializer):
    """Сериализатор модели 'Курс"""
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, obj):
        return (
            obj.lessons.count()
        )  # если в ForeginKey есть related_name - обращаемся по нему(или по obj_set)

    class Meta:
        model = Course
        fields = "__all__"
