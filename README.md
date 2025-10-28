# 🐍 Guia Completo — Criando um Projeto Django com Poetry + GitHub

Este guia ensina **do zero** como criar, configurar e rodar um projeto **Django** usando o **Poetry** para gerenciar dependências e o **GitHub** para versionar o código.  
Ideal pra quem quer um **setup limpo, profissional e pronto pra escalar**. 🚀

---

## 🧩 1. Criar o repositório no GitHub

1. Vá até o [GitHub](https://github.com/new) e clique em **New Repository**.  
2. Escolha o nome (exemplo): `book-store`.  
3. Marque:
   - ✅ **Add a README file**
   - ✅ **Add .gitignore** → selecione **Python**
4. Clique em **Create repository**.

---

## 💻 2. Clonar o repositório

Abra o **PowerShell (Windows)** ou **Terminal (Linux)** e execute:

```bash
git clone https://github.com/seu-usuario/book-store.git
cd book-store
```

---

## ⚙️ 3. Instalar o Poetry

### 🪟 No Windows:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> Após instalar, feche e reabra o terminal, depois teste:

```bash
poetry --version
```

### 🐧 No Linux:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## 🧙 4. Iniciar o projeto com o Poetry

Crie o arquivo `pyproject.toml`:

```bash
poetry init
```

Responda às perguntas interativas.  
Exemplo de resultado final:

```toml
[project]
name = "book-store"
version = "0.1.0"
description = "Book Store API"
authors = [{name = "Renato Minoita", email = "renatornt13@gmail.com"}]
readme = "README.md"
requires-python = ">=3.13"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## 🧩 5. Criar e ativar o ambiente virtual

Crie o ambiente e instale as dependências iniciais:

```bash
poetry install
```

Ative o ambiente:

```bash
poetry shell
```

> ⚠️ Se quiser sair do ambiente:
> ```bash
> exit
> ```

---

## 🧱 6. Instalar Django e Django REST Framework

```bash
poetry add django djangorestframework
```

---

## 🏗️ 7. Criar o projeto Django

Crie o projeto principal:

```bash
poetry run django-admin startproject bookstore .
```

---

## 📦 8. Criar um app dentro do projeto

```bash
poetry run python manage.py startapp api
```

Adicione o app em `bookstore/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
]
```

---

## 🧾 9. Aplicar migrações iniciais

```bash
poetry run python manage.py migrate
```

---

## 🚀 10. Rodar o servidor local

```bash
poetry run python manage.py runserver
```

Acesse: 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧩 11. Criar sua primeira API

### 📁 `api/models.py`

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
```

---

### 🔧 Criar e aplicar migração

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

---

### 🧠 `api/serializers.py`

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

---

### ⚙️ `api/views.py`

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

### 🌐 `api/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

---

### 📡 `bookstore/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

Acesse: 👉 [http://127.0.0.1:8000/api/books/](http://127.0.0.1:8000/api/books/)

---

## 🧰 12. Comandos opcionais úteis

### 🧹 Formatador de código (Black)

```bash
poetry add --dev black
poetry run black .
```

### 🧪 Testes automatizados (Pytest)

```bash
poetry add --dev pytest pytest-django factory-boy
```

Rodar os testes:

```bash
poetry run pytest -v
```

### 🧭 Organização de imports (isort)

```bash
poetry add --dev isort
poetry run isort .
```

### 🧼 Linter (Flake8)

```bash
poetry add --dev flake8
poetry run flake8
```

---

## 📂 13. Estrutura final do projeto

```
book-store/
│
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── bookstore/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── pyproject.toml
├── poetry.lock
├── manage.py
└── README.md
```

---

## 🌳 14. Criar branch e versionar o projeto

```bash
git checkout -b project-setup
git add .
git commit -m "Configuração inicial do projeto Django com Poetry"
git push -u origin project-setup
```

---

## 🔄 15. Criar Pull Request no GitHub

1. Vá até o repositório no GitHub.  
2. Clique em **Compare & pull request**.  
3. Revise e clique em **Create pull request**.  
4. Depois, **Merge pull request** → **Confirm merge**.  
5. (Opcional) Exclua a branch `project-setup`.

---

## 💾 16. Atualizar repositório local após o merge

```bash
git checkout main
git pull origin main
```

---

## 🧠 17. Tabela de comandos Poetry

| Comando | Descrição |
|----------|------------|
| `poetry shell` | Ativa o ambiente virtual |
| `poetry run <cmd>` | Executa comando no ambiente |
| `poetry add <lib>` | Instala dependência |
| `poetry remove <lib>` | Remove dependência |
| `poetry install` | Instala dependências do projeto |
| `poetry update` | Atualiza todas as libs |
| `poetry export -f requirements.txt --output requirements.txt` | Gera arquivo compatível com pip |

---

## ✅ Projeto concluído!

Seu ambiente **Django + REST + Poetry** está configurado com GitHub, pronto para desenvolver APIs profissionais.  
Hora de codar com estilo 😎🔥

---

📘 **Autor:** _Renato Minoita_  
💻 **Tecnologias:** Django • Django REST Framework • Poetry • GitHub  
📅 **Atualizado:** Outubro de 2025  
