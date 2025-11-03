from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from educations.models import Lesson
from educations.paginators import MyPagination
from educations.serializers import LessonSerializer


class LessonCreateList(generics.ListCreateAPIView):
    """Viewset для создания и просмотра урока или списков урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Распределение прав пользователя и модератора
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """Автоприсваиание автора - владельца"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Кто может смотреть все курсы или только свои"""
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Viewset для обновления и удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Кто может смотреть все уроки или только свои"""
        if (
            self.request.user.is_staff
            or self.request.user.groups.filter(name="Moderator").exists()
        ):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)
