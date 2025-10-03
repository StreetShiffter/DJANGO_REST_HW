import re
from rest_framework import serializers


# def CorrectVideoUrl(value):
#     """Валидатор для проверки отношения видео к определенному ресурсу - использовать в сериализаторе отдельным полем"""
#     youtube_regex = r'(https?://)?(www\.|m\.)?(youtube\.com)/.+$'
#
#     if not re.match(youtube_regex, value):
#         raise serializers.ValidationError("Ссылка должна быть на видео с YouTube.")
#
#     return value

class CorrectVideoUrl:
    """Проверяет, что video_url — это ссылка на YouTube"""
    def __init__(self, field):
        self.field = field
        self.__fields__ = [field]

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value:  # пропускаем, если пусто — пусть required решает
            return attrs

        youtube_regex = r'https?://(?:www\.|m\.)?youtube\.com/'
        if not re.search(youtube_regex, value):
            raise serializers.ValidationError({
                self.field: "Ссылка должна быть на видео с YouTube."
            })


class MatchVideoUrl:
    """Проверяет, что в текстовом поле (title/description) НЕТ ссылок на YouTube"""
    def __init__(self, field):
        self.field = field
        self.__fields__ = [field]

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value or not isinstance(value, str):
            return attrs  # пропускаем, если нет значения или не строка

        youtube_regex = r'https?://(?:www\.|m\.)?youtube\.com/'
        if re.search(youtube_regex, value):
            raise serializers.ValidationError({
                self.field: "Текст не должен содержать ссылки на YouTube."
            })

