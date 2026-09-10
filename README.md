# 📬 Newsletter Subscription API

A lightweight, production-ready REST API built with **Django** and **Django REST Framework** that lets any product collect newsletter subscribers. Deploy it once on Render and plug it into any frontend or service via a single HTTP call.

---

## ✨ Features

| Feature | Detail |
|---|---|
| **Subscribe endpoint** | `POST /api/subscribe/` |
| **Duplicate prevention** | Emails are unique — re-submitting the same address returns a 400 |
| **Email normalisation** | All emails are lowercased and trimmed before storage |
| **Rate limiting** | 5 requests / minute per IP (protects against spam) |
| **PostgreSQL backend** | Production-grade relational storage with SSL enforced |
| **Interactive API docs** | Swagger UI at `/api/docs/` and ReDoc at `/api/redoc/` |
| **One-click deploy** | `render.yaml` included for instant Render deployment |

---

## 🏗️ Project Structure

```
newsletter_system/
├── manage.py
├── requirements.txt
├── render.yaml              # Render deployment config
├── .env.example             # Environment variable template
├── system/                  # Django project config
│   ├── settings.py
│   ├── urls.py              # Root URL conf (includes Swagger routes)
│   ├── wsgi.py
│   └── asgi.py
└── subscribe_service/       # Newsletter app
    ├── models.py            # NewsletterSubscriber model
    ├── serializers.py       # Input validation + email normalisation
    ├── views.py             # SubscribeView (POST)
    ├── urls.py              # /subscribe/ route
    ├── throttles.py         # 5/min rate limit
    └── migrations/
```

---

## 🗄️ Data Model

```python
class NewsletterSubscriber(models.Model):
    email           # unique, required
    is_active       # bool, default False
    created_at      # auto timestamp
    confirmed_at    # nullable — set when email is confirmed
    subscribed_at   # nullable
    unsubscribed_at # nullable
```

---

## 🚀 API Reference

### Base URL

| Environment | Base URL |
|---|---|
| Local | `http://localhost:8000` |
| Production (Render) | `https://your-app.onrender.com` |

---

### `POST /api/subscribe/`

Subscribe an email address to the newsletter.

**Request**

```http
POST /api/subscribe/
Content-Type: application/json
```

```json
{
  "email": "user@example.com"
}
```

**Responses**

| Status | Meaning | Example body |
|---|---|---|
| `201 Created` | Subscribed successfully | `{"message": "Successfully Subscribed to newsletter"}` |
| `400 Bad Request` | Invalid or duplicate email | `{"email": ["newsletter subscriber with this email already exists."]}` |
| `429 Too Many Requests` | Rate limit hit (5/min) | `{"detail": "Request was throttled."}` |

**cURL example**

```bash
curl -X POST https://your-app.onrender.com/api/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{"email": "hello@example.com"}'
```

**JavaScript (fetch) example**

```javascript
const res = await fetch("https://your-app.onrender.com/api/subscribe/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "hello@example.com" }),
});
const data = await res.json();
console.log(data);
```

**Python (requests) example**

```python
import requests

response = requests.post(
    "https://your-app.onrender.com/api/subscribe/",
    json={"email": "hello@example.com"},
)
print(response.status_code, response.json())
```

---

## 📖 Interactive Docs (Swagger)

Once deployed (or running locally) visit:

| UI | URL |
|---|---|
| **Swagger UI** | `/api/docs/` |
| **ReDoc** | `/api/redoc/` |
| **Raw OpenAPI schema (JSON)** | `/api/schema/` |

> [!TIP]
> Swagger UI lets you test the endpoint directly in the browser — just click **POST /api/subscribe/** → **Try it out**.

---

## ⚙️ Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL (local instance, or use a free [Neon](https://neon.tech) / [Supabase](https://supabase.com) cloud DB)

### 1 — Clone & install

```bash
git clone https://github.com/your-username/newsletter_system.git
cd newsletter_system

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2 — Configure environment

```bash
cp .env.example .env
# Open .env and fill in your DB credentials and SECRET_KEY
```

```.env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=newsletter_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

### 3 — Run migrations & start

```bash
python manage.py migrate
python manage.py runserver
```

The API is now live at `http://localhost:8000`.  
Swagger UI → `http://localhost:8000/api/docs/`

---

## ☁️ Deploy to Render

> [!IMPORTANT]
> You need a PostgreSQL database. Render offers a **free** managed Postgres instance, or you can use [Neon](https://neon.tech) (generous free tier, SSL-enabled).

### Option A — One-click via `render.yaml`

1. Push this repo to GitHub / GitLab.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your repo — Render reads `render.yaml` automatically.
4. Fill in the database env vars (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`) in the Render dashboard.
5. Click **Apply** — Render builds, runs migrations, and deploys.

### Option B — Manual Web Service

1. **New** → **Web Service** → connect your repo.
2. Set these values in the Render UI:

| Field | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn system.wsgi:application --bind 0.0.0.0:$PORT` |

3. Add the following **Environment Variables**:

| Key | Value |
|---|---|
| `SECRET_KEY` | Generate a strong random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `DB_NAME` | Your Postgres DB name |
| `DB_USER` | Your Postgres user |
| `DB_PASSWORD` | Your Postgres password |
| `DB_HOST` | Your Postgres host |
| `DB_PORT` | `5432` |

4. Hit **Create Web Service** and wait for the first deploy to finish.

> [!NOTE]
> After the first deploy your API is reachable at `https://your-app.onrender.com/api/subscribe/`  
> and docs at `https://your-app.onrender.com/api/docs/`.

---

## 🔒 Rate Limiting

The subscribe endpoint uses Django REST Framework's anonymous throttle keyed by IP address.

| Setting | Value |
|---|---|
| Scope | `subscription_service` |
| Limit | **5 requests / minute** |
| Storage | In-memory (per process) |

Adjust the limit in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'subscription_service': '10/min',  # change as needed
    },
}
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.1 + Django REST Framework 3.18 |
| Database | PostgreSQL (via psycopg2-binary) |
| API Docs | drf-spectacular (OpenAPI 3.1 / Swagger) |
| WSGI Server | Gunicorn |
| Static files | WhiteNoise |
| Config | python-dotenv |

---

## 🤝 Contributing

1. Fork the repo and create a feature branch.
2. Run the existing tests: `python manage.py test`
3. Open a pull request.

---

## 📄 License

MIT — use freely, attribution appreciated.
