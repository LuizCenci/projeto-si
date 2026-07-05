from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Count, Q

from .forms import AvaliacaoEstresseForm, LoginForm, RespostaEstudanteForm, FEATURE_FIELDS
from .models import FormularioGerado, RespostaEstudante
from .services import prever_nivel_estresse, prever_com_features


class HomeView(View):
    template_name = "core/inicio.html"

    def get(self, request):
        return render(request, self.template_name)


class QuestionarioEstresseView(View):
    template_name = "core/home.html"

    def get(self, request):
        form = AvaliacaoEstresseForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AvaliacaoEstresseForm(request.POST)
        resultado = None
        if form.is_valid():
            avaliacao = form.save(commit=False)
            dados_para_predicao = {
                "horas_sono": avaliacao.horas_sono,
                "carga_estudo": avaliacao.carga_estudo,
                "frequencia_dor_cabeca": avaliacao.frequencia_dor_cabeca,
                "nivel_atividade_fisica": avaliacao.nivel_atividade_fisica,
                "qualidade_sono": avaliacao.qualidade_sono,
                "nivel_ansiedade": avaliacao.nivel_ansiedade,
                "pressao_prazos": avaliacao.pressao_prazos,
                "frequencia_cansaco": avaliacao.frequencia_cansaco,
            }
            predicao = prever_nivel_estresse(dados_para_predicao)
            avaliacao.nivel_estresse_previsto = predicao.nivel
            avaliacao.mensagem_explicativa = predicao.mensagem
            avaliacao.score_confianca = predicao.confianca
            avaliacao.save()
            resultado = {
                "nivel": predicao.nivel,
                "nivel_display": avaliacao.get_nivel_estresse_previsto_display(),
                "mensagem": predicao.mensagem,
                "confianca": round(predicao.confianca * 100),
                "nome": avaliacao.nome_estudante,
            }
            form = AvaliacaoEstresseForm()
        return render(request, self.template_name, {"form": form, "resultado": resultado})


class LoginView(View):
    template_name = "core/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("core:dashboard")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("core:home")


@method_decorator(login_required, name="dispatch")
class DashboardView(View):
    template_name = "core/dashboard.html"

    def get(self, request):
        formularios = FormularioGerado.objects.filter(criado_por=request.user)
        total_respostas = RespostaEstudante.objects.filter(
            formulario__in=formularios
        ).count()
        respostas = RespostaEstudante.objects.filter(
            formulario__in=formularios
        ).select_related("formulario")

        distribuicao = (
            respostas.values("nivel_risco")
            .annotate(total=Count("id"))
            .order_by("nivel_risco")
        )

        turmas = (
            respostas.values("turma")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        request_schema = request.scheme
        request_host = request.get_host()
        base_url = f"{request_schema}://{request_host}"

        return render(request, self.template_name, {
            "formularios": formularios,
            "total_respostas": total_respostas,
            "respostas": respostas[:50],
            "distribuicao": distribuicao,
            "turmas": turmas,
            "base_url": base_url,
        })

    def post(self, request):
        if "gerar_formulario" in request.POST:
            formulario = FormularioGerado.objects.create(criado_por=request.user)
            return redirect("core:dashboard")
        return self.get(request)


class FormularioEstudanteView(View):
    template_name = "core/formulario_estudante.html"

    def _get_formulario(self, pk):
        formulario = get_object_or_404(FormularioGerado, pk=pk)
        if not formulario.esta_valido():
            return None
        return formulario

    def _ja_respondeu(self, formulario, ra):
        return RespostaEstudante.objects.filter(formulario=formulario, ra=ra).exists()

    def get(self, request, pk):
        formulario = self._get_formulario(pk)
        if formulario is None:
            return render(request, "core/formulario_expirado.html", status=410)
        form = RespostaEstudanteForm()
        return render(request, self.template_name, {
            "form": form,
            "formulario": formulario,
        })

    def post(self, request, pk):
        formulario = self._get_formulario(pk)
        if formulario is None:
            return render(request, "core/formulario_expirado.html", status=410)

        ra = request.POST.get("ra", "")
        if self._ja_respondeu(formulario, ra):
            return render(request, self.template_name, {
                "form": RespostaEstudanteForm(),
                "formulario": formulario,
                "ja_respondeu": True,
            })

        form = RespostaEstudanteForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.formulario = formulario

            for f in FEATURE_FIELDS:
                v = getattr(resposta, f)
                if v is None:
                    setattr(resposta, f, 2)

            features = [getattr(resposta, f) for f in FEATURE_FIELDS]
            nivel_predito, nivel_risco = prever_com_features(features)
            resposta.nivel_estresse_predito = nivel_predito
            resposta.nivel_risco = nivel_risco
            resposta.save()

            return render(request, self.template_name, {
                "form": RespostaEstudanteForm(),
                "formulario": formulario,
                "resultado": {
                    "nome": resposta.nome_aluno,
                    "nivel": nivel_predito,
                    "nivel_risco": nivel_risco,
                    "mensagem": {
                        0: "Continue mantendo seus habitos saudaveis!",
                        1: "Fique atento aos sinais. Considere buscar apoio.",
                        2: "E recomendado buscar ajuda profissional.",
                    }.get(nivel_predito, ""),
                },
            })

        return render(request, self.template_name, {
            "form": form,
            "formulario": formulario,
        })
