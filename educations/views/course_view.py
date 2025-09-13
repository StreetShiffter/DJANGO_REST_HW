from educations.models import Course
from educations.serializers import CourseSerializer, LessonSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

class CourseViewSet(viewsets.ViewSet):
    """ViewSet-класс для вывода списка курсов и информации по одному объекту
    ModelViewSet - достаточен для передачи queryset и serializer и все работает из коробки"""
    def list(self, request):
        """Показ списка"""
        queryset = Course.objects.all()# достаем объекты из БД
        serializer_class = CourseSerializer(queryset, many=True) # прописываем сериализатору queryset и параметр списка
        return Response(serializer_class.data)


    def create(self, request):
        """Создание объекта"""
        serializer = CourseSerializer(data=request.data)# Передача информации из запроса
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Показ конкретного объекта"""
        queryset = Course.objects.all()# достаем объекты из БД
        course_item = get_object_or_404(queryset, pk=pk)# достаем конкретный объект
        serializer_class = CourseSerializer(course_item)# прописываем сериализатору объект
        return Response(serializer_class.data)


    def update(self, request, pk=None):
        """Редактирование объекта"""
        queryset = Course.objects.all()# достаем объекты из БД
        course_item = get_object_or_404(queryset, pk=pk)# достаем конкретный объект
        serializer = CourseSerializer(course_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


    def partial_update(self, request, pk=None):
        """Редактирование конкретного поля объекта"""
        queryset = Course.objects.all()  # достаем объекты из БД
        course_item = get_object_or_404(queryset, pk=pk)  # достаем конкретный объект
        serializer = CourseSerializer(course_item,
                                      data=request.data,
                                      partial=True)# передача объекта, запроса и параметр частичного изменения
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


    def destroy(self, request, pk=None):
        """Удаление конкретного объекта"""
        queryset = Course.objects.all()  # достаем объекты из БД
        course_item = get_object_or_404(queryset, pk=pk)
        course_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)