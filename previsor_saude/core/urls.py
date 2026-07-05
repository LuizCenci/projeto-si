from django.urls import path
from .views import AvaliacoesUniversidadeView, QuestionarioEstresseView

app_name = "core"

urlpatterns = [
    path("", QuestionarioEstresseView.as_view(), name="home"),
    path("avaliacoes/", AvaliacoesUniversidadeView.as_view(), name="avaliacoes"),
]
