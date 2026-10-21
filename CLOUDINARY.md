# Add Cloudinary to this Django project

Cloudinary stores **uploaded images and videos**. It does not replace the HTML templates or local CSS already in this project.

This app has no media uploads yet. After these steps, Django will send `ImageField` files to Cloudinary and templates can show them with `{{ photo.image.url }}`.

## 1. Create a Cloudinary account

1. Sign up at [https://cloudinary.com](https://cloudinary.com).
2. Open the dashboard and copy:
   - Cloud name
   - API key
   - API secret

Do not commit these values to git. Use environment variables.

## 2. Install packages

```bash
pip install cloudinary django-cloudinary-storage Pillow
```

Add them to `requirements.txt` as well:

```text
cloudinary
django-cloudinary-storage
Pillow
```

## 3. Configure `config/settings.py`

Add the apps. Keep `django.contrib.staticfiles` first so Cloudinary is used only for uploads, not for CSS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'pages',
]
```

Point Django 5.1 media storage at Cloudinary:

```python
import os

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY': os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET': os.environ['CLOUDINARY_API_SECRET'],
}

MEDIA_URL = '/media/'

STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
```

Locally, put those values in a `.env` file at the project root (copy `.env.example`). `settings.py` loads that file with `python-dotenv`. `.env` is gitignored, so keys stay off git.

```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

You can also export the same names in the shell instead of using a `.env` file.

You can also use a single `CLOUDINARY_URL`:

```bash
export CLOUDINARY_URL=cloudinary://your_api_key:your_api_secret@your_cloud_name
```

If both `CLOUDINARY_STORAGE` in settings and env vars are set, the values in `settings.py` win.

## 4. Add a model

In `pages/models.py`:

```python
from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.title
```

Register it in `pages/admin.py` so you can upload from `/admin/`:

```python
from django.contrib import admin

from .models import Photo

admin.site.register(Photo)
```

Then apply the migration:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 5. Show the image in a template

```html
<img src="{{ photo.image.url }}" alt="{{ photo.title }}">
```

That URL is a Cloudinary CDN link.

## What to keep local

Leave CSS and other project assets in `static/`. Only user uploads should go to Cloudinary.
