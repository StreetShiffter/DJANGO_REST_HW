from django.db import models

from users.models import User


class Course(models.Model):
    """Класс курса"""

    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="course_previews/", verbose_name="Превью", blank=True, null=True
    )

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              related_name="owner_course",
                              verbose_name="Владелец",
                              help_text = "Укажите владельца")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Класс урока"""

    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lesson_previews/", verbose_name="Превью", blank=True, null=True
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="URL видео на YouTube"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              related_name="owner_lesson",
                              verbose_name="Владелец",
                              help_text="Укажите владельца")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]  # Уроки будут сортироваться по порядку добавления

    def __str__(self):
        return f"{self.title} ({self.course.title})"
