
# Sistema Inteligente de Monitoramento de Estresse Estudantil

## 🏫 Instituição e Disciplina
* **Universidade:** Universidade Tecnológica Federal do Paraná (UTFPR) – Câmpus Dois Vizinhos
* **Curso:** Bacharelado em Engenharia de Software
* **Disciplina:** Sistemas Inteligentes Aplicados
* **Professor:** Prof. Francisco Carlos Souza

## 👥 Integrantes do Grupo
* Luiz A. Cenci (RA: 2554712)
* Matheus de Aquino (RA: 2554747)
* Murilo Ghedin Ghizzi (RA: 2580608)
* Lucas H. Bonissoni (RA: 2554704)
* Mauro Cella (RA: 258058)

---

## 📌 1. Definição do Problema

### Domínio
Engenharia de Software aplicada à Gestão Educacional e Bem-Estar Acadêmico.

### O Problema
O ambiente universitário impõe uma alta carga de estresse aos estudantes devido a cobranças de prazos, rotina intensa de estudos e privação de sono. Instituições de ensino e coordenadores de curso frequentemente enfrentam dificuldades para identificar alunos em situação de vulnerabilidade psicológica de forma precoce. A falta de intervenção tempestiva costuma resultar em:
* Altas taxas de reprovação;
* Trancamentos de matrícula;
* Abandono/evasão do curso.

As avaliações psicológicas tradicionais, embora eficazes, são demoradas, caras e dependem exclusivamente da iniciativa do próprio aluno em buscar ajuda, o que retarda o suporte necessário.

### Como a IA Resolve
O sistema inteligente atuará como um **monitor preditivo de bem-estar**. Através de um portal acadêmico (MVP com interface Web), o estudante responderá a um questionário rápido sobre seus hábitos e sintomas recentes. 

O módulo de Inteligência Artificial processará esses dados comportamentais e físicos, classificando o nível de estresse do aluno em três categorias:
* **Baixo**
* **Médio**
* **Alto**

Com base nessa classificação, o sistema poderá acionar alertas preventivos automaticamente para a coordenação/corpo pedagógico e sugerir canais de apoio diretamente ao estudante.

---

## 🔍 2. Pesquisa e Benchmark

### Soluções Existentes
Os sistemas acadêmicos atuais são predominantemente administrativos, focados apenas no registro de notas, frequências e histórico escolar. Não há registros de módulos inteligentes comerciais integrados que cruzem variáveis de saúde, sintomas físicos e rotina diária para mapear o perfil psicossocial do estudante de forma ativa.

### Técnicas de IA Aplicáveis
O projeto utilizará **Aprendizado de Máquina Supervisionado** focado em problemas de **Classificação**. Serão avaliados e implementados algoritmos clássicos para dados tabulares estruturados:
* **Decision Trees (Árvores de Decisão)**
* **K-Nearest Neighbors (KNN)**

A implementação será feita em Python utilizando a biblioteca **scikit-learn**. Essa abordagem permite consumir dados tabulares de fácil tratamento e expor o modelo treinado através de uma API simples para consumo do front-end Web.

### Base de Dados Selecionada
* **Dataset:** *Student Stress Monitoring Datasets*
* **Origem:** Disponível publicamente no Kaggle.
* **Características:** A base simula e coleta dados de monitoramento contínuo de estudantes, fornecendo a estrutura ideal em formato CSV para o treinamento e teste de modelos de classificação supervisionada.

---

## 🛠️ Tecnologias Previstas
* **Linguagem:** Python
* **Biblioteca de IA:** `scikit-learn`, `pandas`, `numpy`
* **Formato dos Dados:** CSV
* **Interface:** Web (MVP)

---
Este repositório armazena a documentação e os artefatos de código para o desenvolvimento e validação do modelo preditivo de estresse acadêmico.
README.md
Exibindo README.md.