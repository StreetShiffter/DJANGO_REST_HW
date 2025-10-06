from rest_framework.permissions import IsAuthenticated, IsAdminUser

from educations.models import Course
from educations.paginators import MyPagination
from educations.serializers import CourseSerializer, CourseSerializerList

from rest_framework import viewsets

from users.permissions import IsOwnerOrModerator


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для вывода списка курсов и информации по одному объекту
    ModelViewSet - достаточен для передачи queryset и serializer и все работает из коробки
    """

    # queryset = (
    #     Course.objects.all()
    # )  # Достаем объекты из БД(убираем сериализатор т.к. есть метод)
    permission_classes = [IsAuthenticated,  IsOwnerOrModerator, IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_serializer_class(self):
        """Метод ловит действие 'retrieve', то перенаправляет на другой сериализатор"""
        if self.action in ['list', 'retrieve']:
            return CourseSerializerList
        return CourseSerializer

    def get_queryset(self):
        """Кто может смотреть все уроки или только свои"""
        if self.request.user.groups.filter(name='Moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Автоприсваиание автора - владельца"""
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # важно для доступа к user
        return context

