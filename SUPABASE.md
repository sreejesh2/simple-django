# Use Supabase Postgres with this Django project

This project uses Supabase Postgres with separate `.env` keys. You do not need the Supabase JS client or REST API for this.

## 1. Create a Supabase project

1. Sign up at [https://supabase.com](https://supabase.com) and create a project.
2. Open the dashboard → **Connect**.
3. Copy the **Session pooler** URI (port `5432`).

That connection is the safest for Django on a normal IPv4 network (a Mac, home Wi-Fi, most hosts).

Avoid the **Transaction pooler** (port `6543`) for Django. It can break migrations because of prepared statements.

The URI looks like:

```text
postgresql://postgres.xxxx:YOUR_PASSWORD@aws-0-ap-south-1.pooler.supabase.com:5432/postgres
```

Do not commit the password. Use environment variables.

## 2. Install the Postgres driver

```bash
pip install "psycopg[binary]"
```

Add it to `requirements.txt` as well:

```text
psycopg[binary]
```

## 3. Put the values in `.env`

```bash
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres.xxxx
SUPABASE_DB_PASSWORD=your_password
SUPABASE_DB_HOST=aws-0-ap-northeast-2.pooler.supabase.com
SUPABASE_DB_PORT=5432
```

`settings.py` reads them with `os.environ.get(...)`. Use the **Session pooler** host from the dashboard.

## 4. Run migrations against Supabase

```bash
python manage.py migrate
```

Django will create `auth_*`, `django_*`, and later your own tables in the Supabase database.

## How this fits with Cloudinary

| Thing | Where it lives |
|---|---|
| Users, pages, photo records | Supabase Postgres |
| Image files | Cloudinary |
| CSS / templates | This repo (`static/`, `templates/`) |

A `Photo` row would store `title` and the Cloudinary image path in Postgres. The file itself stays on Cloudinary.

See `CLOUDINARY.md` for the image-upload setup.
