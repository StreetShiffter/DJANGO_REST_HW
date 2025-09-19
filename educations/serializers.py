from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from educations.models import Course, Lesson

class LessonSerializer(ModelSerializer):
    """Сериализатор модели 'Урок"""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializerList(ModelSerializer):
    """Сериализатор модели 'Курс' для показа количества уроков"""
    count_lessons = SerializerMethodField()# поля могут быть __all__
    # показ информации уроков в курсе(обязательно в перечислении полей т.к. это внешний сериализатор[использовать related_name])
    lessons = LessonSerializer(many= True, read_only=True)# many = уроков может быть несколько(берем сериализатор урока)

    def get_count_lessons(self, obj):
        return obj.lessons.count()# если в ForeginKey есть related_name - обращаемся по нему(или по obj_set)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'count_lessons',
            'lessons',
        ]


class CourseSerializer(ModelSerializer):
    """Сериализатор модели 'Курс"""

    class Meta:
        model = Course
        fields = '__all__'
