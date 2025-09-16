from educations.models import Lesson
from educations.serializers import LessonSerializer
from rest_framework import generics

#Возможно объединять несколько классов вместе(если не переопределять методы)
class LessonCreateList(generics.ListCreateAPIView):
    """Показ списка уроков и создание"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Изменение объекта полное или частичное, а так же его удаление"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

