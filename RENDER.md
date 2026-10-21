# Host this Django project on Render (student guide)

This is a simple class demo, not a production setup.

**What each service does**

| Service | Job |
|---|---|
| Render | Runs the Django website on the internet |
| Supabase | Stores data (Postgres) |
| Cloudinary | Stores uploaded images |

Your laptop uses `python manage.py runserver`. Render cannot use that. It uses a small server called **Gunicorn** instead.

## 1. Add two packages

Students already have Django, Cloudinary, and Supabase. For Render, also add:

```text
gunicorn
psycopg[binary]
```

`gunicorn` starts the site on Render.  
`psycopg` lets Django talk to Supabase Postgres.

Put them in `requirements.txt` so Render can install them.

## 2. One setting students must change

On your laptop, `ALLOWED_HOSTS = []` is fine.  
On Render, Django needs the website name, or it will block the page.

In `config/settings.py`:

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

That reads the host from an environment variable, same idea as Cloudinary and Supabase.

## 3. Put the code on GitHub

1. Create a GitHub repository.
2. Do **not** upload `.env` (it is already in `.gitignore`).
3. Push the project.

Render reads the code from GitHub.

## 4. Create a Web Service

1. Go to [https://render.com](https://render.com) and sign in (GitHub login is easiest).
2. Click **New** → **Web Service**.
3. Pick this repo.

Use these commands:

| Field | Value | Why |
|---|---|---|
| Build command | `pip install -r requirements.txt` | Installs Django and the other packages |
| Start command | `gunicorn config.wsgi:application` | Starts the site (`config` is this project folder) |

## 5. Copy env vars into Render

Locally those values live in `.env`.  
On Render: open the service → **Environment** → add the same names.

```bash
ALLOWED_HOSTS=your-service.onrender.com

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.your_project_ref
SUPABASE_DB_PASSWORD=
SUPABASE_DB_HOST=aws-0-ap-northeast-2.pooler.supabase.com
SUPABASE_DB_PORT=5432
```

Use the **Session pooler** host and user `postgres.xxxx`.  
Do not use `db.xxxx.supabase.co` (that one is IPv6 and Render cannot reach it).

After the first deploy, Render gives you a URL like `https://something.onrender.com`. Put that host in `ALLOWED_HOSTS`.

## 6. Create the tables

In the Render **Shell**:

```bash
python manage.py migrate
python manage.py createsuperuser
```

`migrate` creates the Django tables in Supabase.  
`createsuperuser` makes an admin login.

## 7. Open the site

Visit `https://your-service.onrender.com/`.

- Home page = Django templates on Render
- Photo rows = Supabase
- Photo files = Cloudinary
- Admin = `/admin/`

## If something fails

- **DisallowedHost** — `ALLOWED_HOSTS` does not match the Render URL.
- **Database error** — wrong host. Use Session pooler, not the direct `db.` host.
- **Site is slow the first time** — free Render apps sleep. The first click wakes them up.

See `SUPABASE.md` and `CLOUDINARY.md` for those parts.
