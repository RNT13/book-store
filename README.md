# 🐍 Guia Completo — Criando Projeto Python com Poetry, Django REST e Git Workflow

Este guia explica como criar e gerenciar um projeto Python/Django com **Poetry**, preparar o ambiente para **pull requests** e **branches**, e automatizar o fluxo de trabalho tanto no **Windows (VS Code)** quanto no **Linux**.

---

## 🚀 1️⃣ Criando o Projeto com Poetry

### 🔹 Instale o Poetry

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**Linux/macOS:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verifique se está funcionando:

```bash
poetry --version
```

> ⚡ Dica: Caso não reconheça o comando no Windows, adicione manualmente ao PATH:
> `C:\Users\<seu_usuario>\AppData\Roaming\Python\Scripts`

---

### 🔹 Criar o projeto Django

```bash
poetry new nome_do_projeto
cd nome_do_projeto
```

Instale o Django e o Django REST Framework:

```bash
poetry add django djangorestframework
```

Crie o projeto base do Django:

```bash
poetry run django-admin startproject core .
```

Crie os apps conforme o exemplo da estrutura:

```bash
poetry run python manage.py startapp nome_do_app
```

---

## 📁 2️⃣ Estrutura de Pastas (Exemplo)

```
nome_do_projeto/
│
├── nome_do_app/
│   ├── migrations/
│   ├── models/
│   ├── serializers/
│   ├── tests/
│   │   └── factories.py
│   ├── apps.py
│   ├── admin.py
│   └── views.py
│
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## 🧠 3️⃣ Usando o Poetry para Gerenciar o Projeto

### Executar comandos Django com Poetry

Não é necessário ativar manualmente o ambiente virtual. Use **`poetry run`** para executar qualquer comando dentro do ambiente isolado:

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Outras operações úteis

```bash
poetry add <pacote>           # Adiciona um pacote
poetry remove <pacote>        # Remove um pacote
poetry install                # Instala dependências do pyproject.toml
poetry update                 # Atualiza pacotes
```

> 💡 Assim, não há necessidade de ativar a virtualenv manualmente nem usar `python` fora do Poetry.

---

## 🌱 4️⃣ Configuração do Git e Branches

### Inicialize o repositório

```bash
git init
git add .
git commit -m "Initial commit"
```

### Crie a branch principal

```bash
git branch -M main
```

### Crie uma branch de feature

```bash
git checkout -b setup_inicial
```

Após terminar a feature:

```bash
git add .
git commit -m "feat: setup inicial"
git push origin setup_inicial
```

---

## 🔄 5️⃣ Preparação para Pull Requests

1. Suba sua branch para o repositório remoto:

   ```bash
   git push -u origin setup_inicial
   ```

2. No GitHub, clique em **Compare & Pull Request**.

3. Adicione título e descrição explicando o que foi alterado.

4. Solicite revisão antes do merge.

---

## 💡 6️⃣ Configuração no VS Code

- Instale as extensões:

  - **Black Formatter**

- Configure o interpretador Python:

  - `Ctrl + Shift + P` → `Python: Select Interpreter`
  - Escolha o ambiente gerenciado pelo Poetry.

---

## 🧰 7️⃣ Comandos úteis

| Tarefa                | Comando                                 |
| --------------------- | --------------------------------------- |
| Instalar dependências | `poetry install`                        |
| Adicionar pacote      | `poetry add <pacote>`                   |
| Rodar servidor Django | `poetry run python manage.py runserver` |
| Rodar migrações       | `poetry run python manage.py migrate`   |
| Rodar testes          | `poetry run python manage.py test`      |
| Atualizar pacotes     | `poetry update`                         |

---

## 📘 8️⃣ Configurando o Django REST Framework

No arquivo `settings.py`, adicione:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'nome_do_app',
]
```

---

## 🧩 9️⃣ Executar o Projeto

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

📘 **Autor:** _Renato Minoita_
💻 **Tecnologia:** Django + Poetry + Git
📅 **Atualizado:** Outubro de 2025
