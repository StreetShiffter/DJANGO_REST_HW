from django.urls import path

from .apps import UsersConfig
from .views import (
    PaymentViewSet,
    UserCreateAPIview,
    UserProfileAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    UserSubscribeAPIView,
)
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payment", PaymentViewSet, basename="payment")


urlpatterns = [
    path("list/", UserListAPIView.as_view(), name="user-list"),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/delete/", UserDeleteAPIView.as_view(), name="user-delete"),
    path("register/", UserCreateAPIview.as_view(), name="register"),
    path("subscribe/", UserSubscribeAPIView.as_view(), name="subscribe"),
    path("subscribe/<int:course_id>/",UserSubscribeAPIView.as_view(), name="subscribe-toggle",),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls
