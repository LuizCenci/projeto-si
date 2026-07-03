from django.urls import path
from .views import QuestionarioEstresseView

app_name = "core"

urlpatterns = [
    path("", QuestionarioEstresseView.as_view(), name="home"),
]
