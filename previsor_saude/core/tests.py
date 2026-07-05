from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import AvaliacaoEstresse, RoleUsuario

Usuario = get_user_model()


class ControleAcessoTests(TestCase):
    def setUp(self):
        self.estudante = Usuario.objects.create_user("12345", password="senha-forte", first_name="Ana", role=RoleUsuario.ESTUDANTE)
        self.universidade = Usuario.objects.create_user("universidade@teste.edu", password="senha-forte", role=RoleUsuario.UNIVERSIDADE)

    def test_role_e_obrigatoria_na_criacao(self):
        with self.assertRaisesMessage(ValueError, "role é obrigatória"):
            Usuario.objects.create_user("sem-role", password="senha-forte")

    def test_estudante_acessa_teste_mas_nao_relatorio(self):
        self.client.force_login(self.estudante)
        self.assertEqual(self.client.get(reverse("core:home")).status_code, 200)
        resposta = self.client.get(reverse("core:avaliacoes"))
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.url, reverse("entrada"))

    def test_universidade_acessa_relatorio_mas_nao_teste(self):
        self.client.force_login(self.universidade)
        self.assertEqual(self.client.get(reverse("core:avaliacoes")).status_code, 200)
        resposta = self.client.get(reverse("core:home"))
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(resposta.url, reverse("entrada"))

    def test_teste_salva_respostas_vinculadas_ao_estudante(self):
        self.client.force_login(self.estudante)
        resposta = self.client.post(reverse("core:home"), {
            "horas_sono": 7, "carga_estudo": 5, "frequencia_dor_cabeca": 2,
            "nivel_atividade_fisica": 3, "qualidade_sono": 4,
            "nivel_ansiedade": 2, "pressao_prazos": 3, "frequencia_cansaco": 2,
        })
        self.assertEqual(resposta.status_code, 200)
        avaliacao = AvaliacaoEstresse.objects.get()
        self.assertEqual(avaliacao.estudante, self.estudante)
        self.assertTrue(avaliacao.nivel_estresse_previsto)

# Create your tests here.
