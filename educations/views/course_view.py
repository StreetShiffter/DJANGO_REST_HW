from educations.models import Course
from educations.serializers import CourseSerializer

from rest_framework import viewsets


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для вывода списка курсов и информации по одному объекту
    ModelViewSet - достаточен для передачи queryset и serializer и все работает из коробки"""
    queryset = Course.objects.all()# достаем объекты из БД
    serializer_class = CourseSerializer
