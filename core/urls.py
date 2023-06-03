from django.urls import path

from core.views import UserCreateView, UserLoginView

# ----------------------------------------------------------------
# urlpatterns
urlpatterns = [
    path('reg/', UserCreateView.as_view()),
    path('auth/', UserLoginView.as_view()),
]
