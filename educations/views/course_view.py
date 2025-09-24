from educations.models import Course
from educations.serializers import CourseSerializer, CourseSerializerList

from rest_framework import viewsets


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для вывода списка курсов и информации по одному объекту
    ModelViewSet - достаточен для передачи queryset и serializer и все работает из коробки
    """

    queryset = (
        Course.objects.all()
    )  # Достаем объекты из БД(убираем сериализатор т.к. есть метод)

    def get_serializer_class(self):
        """Метод ловит действие 'retrieve', то перенаправляет на другой сериализатор"""
        if self.action == "retrieve":
            return CourseSerializerList
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        owner_course = self.request.user
        course.save()

