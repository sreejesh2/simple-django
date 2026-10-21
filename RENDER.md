# Host this Django project on Render (class demo)

This is a simple class demo, not a production setup. The same steps are on the site at `/render/`, with copy buttons.

| Service | Job |
|---|---|
| Render | Runs the Django website |
| Supabase | Stores data (Postgres) |
| Cloudinary | Stores uploaded images |

## 1. Project setup (already done in this repo)

`requirements.txt` includes `gunicorn` (runs Django on the server) and `whitenoise` (serves CSS and JS).

`config/settings.py` has WhiteNoise right after `SecurityMiddleware`, and:

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
ALLOWED_HOSTS = ['*']
```

## 2. Push to GitHub

```bash
git add .
git commit -m "ready for render"
git push origin main
```

`.env` is in `.gitignore`. The keys go into Render, not GitHub.

## 3. Create the Web Service

Render → **+ New** → **Web Service** → pick the GitHub repo. Then fill in the form:

| Field | Value | Why |
|---|---|---|
| Name | `mams-django-workshop` | Becomes `mams-django-workshop.onrender.com` |
| Project | leave as is | Optional grouping only |
| Language | `Python 3` | Django is Python |
| Branch | `main` | Deploys on every push to `main` |
| Region | `Singapore (Southeast Asia)` | Closest to India and to Supabase |
| Root Directory | leave empty | `manage.py` is at the repo root |
| Build Command | see below | Install, collect CSS, create tables |
| Start Command | `gunicorn config.wsgi:application` | `config` holds `wsgi.py` |
| Instance Type | `Free` | Enough for a demo; sleeps when idle |

Build Command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

## 4. Environment variables

On the same form → **Environment Variables** → **Add from .env**, then paste:

```bash
PYTHON_VERSION=3.12.0
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.your_project_ref
SUPABASE_DB_PASSWORD=your_password
SUPABASE_DB_HOST=aws-0-ap-northeast-2.pooler.supabase.com
SUPABASE_DB_PORT=5432
```

Use the Session pooler host and `postgres.xxxx` user. The direct `db.xxxx.supabase.co` host will not connect.

## 5. Deploy

Click **Deploy Web Service**. Wait for **Your service is live**, then open the link.

## 6. Admin login

The free plan has no Render Shell. Laptop and Render share the same Supabase database, so run this on the laptop:

```bash
python manage.py createsuperuser
```

Then log in at `https://your-app.onrender.com/admin/`.

## If something fails

- **Build failed** — a package is missing from `requirements.txt`.
- **No styling** — WhiteNoise missing from `MIDDLEWARE`, or `collectstatic` missing from the build command.
- **Database error** — wrong `SUPABASE_DB_*` values; use the Session pooler.
- **Images don't upload** — check the `CLOUDINARY_*` values.
- **Slow first visit** — the free app was asleep.
