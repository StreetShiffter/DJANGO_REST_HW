from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from educations.models import Course, Lesson

class CourseSerializer(ModelSerializer):
    """Сериализатор модели 'Курс"""

    class Meta:
        model = Course
        fields = '__all__'

class CourseSerializerList(ModelSerializer):
    """Сериализатор модели 'Курс' для показа количества уроков"""
    count_lessons = SerializerMethodField()

    def get_count_lessons(self, obj):
        return obj.lessons.count()# если в ForeginKey есть related_name - обращаемся по нему(или по obj_set)

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    """Сериализатор модели 'Урок"""


    class Meta:
        model = Lesson
        fields = '__all__'