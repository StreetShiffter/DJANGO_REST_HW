from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from config import settings


# from educations.models import Lesson, Course - меняем на lazy model resolution


class CustomUserManager(BaseUserManager):
    """Кастомное правило создание пользователя и суперпользователя"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс создания пользователя"""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Телефон должен быть в формате: '+999999999'. До 15 цифр.",
            )
        ],
        blank=True,
        null=True,
        verbose_name="Телефон",
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="user_avatars/", blank=True, null=True, verbose_name="Аватарка"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # ← Важно! Авторизация по email
    REQUIRED_FIELDS = []  # Нет обязательных полей кроме email и пароля

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель оплаты куросов или уроков"""

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Заменен прямой импорт на ссылку из конфига
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        "educations.Course",  # Заменен прямой импорт на ссылку - защита от циклической загрузки миграции
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    lesson = models.ForeignKey(
        "educations.Lesson",  # Заменен прямой импорт на ссылку - защита от циклической загрузки миграции
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )
    # DecimalField - правильная работа только для денег
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID платежа в Stripe"
    )
    stripe_status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Статус платежа в Stripe"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        """Выбор названия курса или урока на выбор"""
        target = (
            self.course.title
            if self.course
            else (self.lesson.title if self.lesson else "Не указано")
        )
        return f"Платеж {self.amount} от {self.user} за {target}"

    def clean(self):
        """Проверка оплаты - валидация"""
        if not self.course and not self.lesson:
            raise ValidationError("Должен быть указан хотя бы один: курс или урок.")
        if self.course and self.lesson:
            raise ValidationError(
                "Нельзя одновременно указать и курс, и урок. Выберите что-то одно."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # вызываем валидацию перед сохранением
        super().save(*args, **kwargs)


class Subscription(models.Model):
    """Модель подписки пользователя на обновления курса."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        "educations.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscribers",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Указывает, активна ли подписка. Неактивные подписки не получают уведомлений.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания подписки.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего изменения подписки.",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = (
            "user",
            "course",
        )  # Один пользователь может быть подписан на курс только один раз
        ordering = ["-created_at"]

    def __str__(self):
        status = "активна" if self.is_active else "неактивна"
        return f"Подписка {self.user} на курс '{self.course}' ({status})"

    def deactivate(self):
        """Метод для деактивации подписки без её удаления."""
        self.is_active = False
        self.save()

    def activate(self):
        """Метод для повторной активации подписки."""
        self.is_active = True
        self.save()
