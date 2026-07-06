from django.urls import path
from .views import (
    HomeView, QuestionarioEstresseView, LoginView, LogoutView,
    DashboardView, FormularioEstudanteView, DetalhesFormularioView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("legado/", QuestionarioEstresseView.as_view(), name="legado"),
    path("form/<uuid:pk>/", FormularioEstudanteView.as_view(), name="formulario_estudante"),
    path("form/<uuid:pk>/detalhes/", DetalhesFormularioView.as_view(), name="detalhes_formulario"),
]
