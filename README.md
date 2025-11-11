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
requires-python = ">=3.13"

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## 🧩 5. Create and activate the virtual environment

```bash
poetry install
poetry shell
```

Exit:

```bash
exit
```

---

## 🧱 6. Install Django and Django REST Framework

```bash
poetry add django djangorestframework
```

---

## 🏗️ 7. Create the Django project

```bash
poetry run django-admin startproject bookstore .
```

---

## 📦 8. Create an app inside the project

```bash
poetry run python manage.py startapp api
```

Add to `bookstore/settings.py`:

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

## `bookstore/urls.py`

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

Render does **not** use Poetry directly.
You must generate a `requirements.txt` using **pip freeze**.

---

## ✅ Generate `requirements.txt`

```bash
poetry install  # garante que todas dependências estão instaladas
pip freeze > requirements.txt
```

Commit this file to GitHub.

---

## ✅ Install Gunicorn (Render requirement)

```bash
poetry add gunicorn
pip freeze > requirements.txt
```

---

## ✅ Install PostgreSQL driver

Render uses PostgreSQL:

```bash
poetry add psycopg2-binary
pip freeze > requirements.txt
```

---

## ✅ Install and configure `dj-database-url`

```bash
poetry add dj-database-url
```

In `bookstore/settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}
```

---

## ✅ Configure ALLOWED_HOSTS

```python
ALLOWED_HOSTS = ["*"]
```

---

## ✅ Configure STATIC files for production

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## ✅ Create `Procfile` (optional but recommended)

```
web: gunicorn bookstore.wsgi:application
```

---

## ✅ Create `render.yaml` (Highly Recommended)

```yaml
services:
  - type: web
    name: bookstore-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn bookstore.wsgi:application
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_SETTINGS_MODULE
        value: bookstore.settings
databases:
  - name: bookstore-db
    plan: free
```

---

## ✅ Render Deploy Steps

1. Push your project to GitHub
2. Create a free account at [https://render.com](https://render.com)
3. Click **New → Web Service**
4. Connect your GitHub repository
5. Build command:

```
pip install -r requirements.txt
```

6. Start command:

```
gunicorn bookstore.wsgi:application
```

7. After deploy → open **Shell** and run:

```
python manage.py migrate
python manage.py collectstatic --noinput
```

Done ✅

Your Django API is live on Render 🎉

---

# ✅ Author

**Renato Minoita**
Technologies: Django • DRF • Poetry • Render • GitHub
Updated: November 2025
