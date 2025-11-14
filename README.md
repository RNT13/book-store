# 🐍 Complete Guide --- Creating a Django Project with Poetry + GitHub + Render Deployment

This guide teaches you **from scratch** how to create, configure, and
run a **Django** project using **Poetry** for dependency management,
**GitHub** for version control, and **Render** for deployment.
Perfect for those who want a **clean, professional, and scalable
setup**. 🚀

---

## 🧩 1. Create the GitHub repository

1. Go to [https://github.com/new](https://github.com/new) and click **New Repository**.\
2. Choose a name (example): `book-store`.\
3. Check:

   - ✅ **Add a README file**
   - ✅ **Add .gitignore** → choose **Python**

4. Click **Create repository**.

---

## 💻 2. Clone the repository

```bash
git clone https://github.com/your-username/book-store.git
cd book-store
```

---

## ⚙️ 3. Install Poetry

### 🪟 Windows:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Verify:

```bash
poetry --version
```

### 🐧 Linux:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## 🧙 4. Initialize the project with Poetry

```bash
poetry init
```

Example `pyproject.toml`:

```toml
[project]
name = "book-store"
version = "0.1.0"
description = "Book Store API"
authors = [{name = "Renato Minoita", email = "email@exemplo.com"}]
readme = "README.md"
requires-python = ">=3.13,<4.0"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## 🧩 5. Create and activate the virtual environment

```bash
poetry install
poetry env activate
```

---

## 🧱 6. Install Django and Django REST Framework

```bash
poetry add django djangorestframework
```

---

## 🏗️ 7. Create the Django project

```bash
poetry run django-admin startproject core .
```

---

## 📦 8. Create an app inside the project

```bash
poetry run python manage.py startapp api
```

Add to `core/settings.py`:

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

## 🧾 9. Apply initial migrations

```bash
poetry run python manage.py migrate
```

---

## 🚀 10. Run the development server

```bash
poetry run python manage.py runserver
```

---

## 🧩 11. Create your first API

### `api/models.py`

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
```

Run:

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

---

## `api/serializers.py`

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

---

## `api/views.py`

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

---

## `api/urls.py`

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

## `core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

---

# ✅ 12. Adding Render Deployment Configuration (Very Important)

The Render can deploy directly from a Dockerfile, which simplifies the process. To do this, we need some dependencies and configuration files.

---

## ✅ Generate `requirements.txt`

```bash
poetry install  # garante que todas dependências estão instaladas
pip freeze > requirements.txt
```

## ✅ Install the `dempendencies`

```bash
poetry add gunicorn psycopg2-binary dj-database-url whitenoise poetry-plugin-export
```

## ✅ Generate the `requirements.txt`

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

In `core/settings.py`:

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}
```

---

### Create the `.env.dev` file

Create in the root:

```env
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=127.0.0.1 localhost backend-django-oaig.onrender.com
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=bookstore_dev_db
SQL_USER=bookstore_dev
SQL_PASSWORD=bookstore123
SQL_HOST=db
SQL_PORT=5432
```

---

## ✅ Configure the ALLOWED_HOSTS (DEV + Render)

### 📌 settings.py

```python
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1 localhost"
).split()

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

### How it works

- In **dev**, use only the values in `.env.dev`.
- On **Render**, it automatically adds the public hostname.
- Allows multiple hosts.

---

## ✅ Configure STATIC files for production

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## ✅ Create `Dockerfile`

```dockerfile
# Dockerfile

FROM python:3.13-slim

# Configurações básicas
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o projeto
COPY . .

# Variáveis para o Render
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PORT=8000

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Rodar Gunicorn em produção com as migrações feitas
CMD ["bash", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
```

---

## ✅ Create `Docker-compose.yaml`

```yaml
services:
  db:
    image: postgres:16.0-alpine
    ports:
      - 5433:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=bookstore_dev
      - POSTGRES_PASSWORD=bookstore123
      - POSTGRES_DB=bookstore_dev_db

  web:
    build:
      context: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - app_data:/usr/src/app
    ports:
      - 8000:8000
    env_file:
      - .env.dev
    depends_on:
      - db

volumes:
  postgres_data:
  app_data:
```

---

## ✅ Create `render.yaml` (Highly Recommended)

```yaml
services:
  - type: web
    name: backend-django
    env: docker
    dockerfilePath: ./Dockerfile
    plan: free
    envVars:
      - key: SECRET_KEY
        generateValue: true # Generate a random secret key
      - key: DEBUG
        value: "0"
      - key: DJANGO_ALLOWED_HOSTS # Set the DJANGO_ALLOWED_HOSTS environment variable
        value: backend-django.onrender.com # Replace with your desired value
      - key: DATABASE_URL
        fromDatabase:
          name: db
          property: connectionString

databases:
  - name: db
    plan: free
```

---

## ✅ 13. Steps to Deploy on Render

With the `render.yaml` file in your repository, the process is very straightforward:

1.  **Push everything to GitHub**:
    ```bash
    git add .
    git commit -m "Configure Docker and Render for deployment"
    git push origin main
    ```
2.  Create a free account at [https://render.com](https://render.com).
3.  On the dashboard, click **New → Blueprint**.
4.  Connect your project's repository. Render will automatically detect and use the `render.yaml` file.
5.  Click **Apply** to confirm and start the deployment.

Render will build the Docker image, create the database, and launch your application. The `CMD` in the `Dockerfile` ensures that migrations are applied on every new deployment.

Done! ✅ Your Django API is live on Render. 🎉

---

# ✅ Author

**Renato Minoita**
Technologies: Django • DRF • Poetry • Render • GitHub
Updated: November 2025
