from django.shortcuts import render
from django.views import View

from .forms import AvaliacaoEstresseForm
from .services import prever_nivel_estresse


class QuestionarioEstresseView(View):
    """
    View única (baseada em classe) que exibe o formulário e, no POST,
    processa a resposta, delega a predição ao serviço de IA (services.py)
    e renderiza o resultado na MESMA página.
    """

    template_name = "core/home.html"

    def get(self, request):
        form = AvaliacaoEstresseForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AvaliacaoEstresseForm(request.POST)
        resultado = None

        if form.is_valid():
            avaliacao = form.save(commit=False)

            # A view NÃO conhece a lógica de IA: apenas chama o serviço.
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
            # Novo formulário em branco para uma próxima avaliação.
            form = AvaliacaoEstresseForm()

        return render(
            request,
            self.template_name,
            {"form": form, "resultado": resultado},
        )
