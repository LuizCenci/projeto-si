# Previsor de Bem-Estar Acadêmico (MVP)

Aplicação Django que simula um sistema de **monitoramento preditivo de
estresse acadêmico**. O estudante responde a um questionário rápido e o
backend consome uma predição (simulada localmente, mas pronta para se
conectar a um modelo de IA já treinado) que classifica o nível de
estresse em **Baixo**, **Médio** ou **Alto**.

> Este projeto **não treina** nenhum modelo de IA e **não baixa** o
> dataset do Kaggle. Toda a lógica de predição está isolada em
> `core/services.py`, pronta para ser trocada por uma chamada real a uma
> API/modelo treinado offline com o *Student Stress Monitoring Datasets*.

## Estrutura do projeto

```
previsor_saude/
├── manage.py
├── requirements.txt
├── config/                  # projeto Django (settings, urls raiz)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/                    # app principal
    ├── models.py            # AvaliacaoEstresse (armazena respostas + resultado)
    ├── forms.py             # AvaliacaoEstresseForm (ModelForm do questionário)
    ├── views.py              # QuestionarioEstresseView (CBV)
    ├── services.py           # lógica/serviço de predição (isolado da view)
    ├── admin.py              # registro no Django Admin
    ├── urls.py                # rotas do app
    ├── migrations/
    ├── templates/core/
    │   ├── base.html
    │   └── home.html         # formulário + resultado na mesma página
    └── static/core/css/
        └── style.css          # CSS próprio, sem frameworks externos
```

## Como rodar

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar as migrations

```bash
python manage.py migrate
```

### 4. Criar um superusuário (para acessar o Django Admin)

```bash
python manage.py createsuperuser
```

### 5. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse:

- **Aplicação:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Conectando um modelo de IA real no futuro

Em `core/services.py`, a função `prever_nivel_estresse(dados)` é o único
ponto de contato entre o Django e a IA. Para plugar um modelo real:

1. Implemente/ajuste `_prever_via_api()` para chamar o endpoint do
   modelo já treinado (ex.: `requests.post(...)`).
2. Em `config/settings.py`, defina:
   ```python
   STRESS_PREDICTOR_USE_API = True
   STRESS_PREDICTOR_API_URL = "https://seu-endpoint/predict"
   ```

Nenhuma outra parte do sistema (view, template, models) precisa mudar.
