# High-Level Secure Performance Auth

A production‑grade authentication system built with **Django**, **Django REST Framework**, **JWT**, **JWE**, **HttpOnly Cookies**, **Celery**, **Redis**, and **RabbitMQ**. The project focuses on **security**, **performance**, and **scalability**, providing a solid foundation for modern backend systems.

---

## 🚀 Features

### 🔐 Security & Authentication

* JWT **Access** & **Refresh** tokens
* **JWE (JSON Web Encryption)** for secure transport of JWT
* **HttpOnly**, **Secure**, **SameSite=Strict** cookies
* **Token Rotation** & **Blacklist** mechanism
* IP & Client Fingerprint checks (middleware)
* Email Verification & Password Reset
* Google OAuth2 Login

### ⚙️ Architecture

* Modular Django apps structure
* Celery worker + periodic scheduled tasks
* RabbitMQ as message broker
* Redis for caching & Celery backend
* Fully containerized with Docker
* Ready for production with separate `dev` and `prod` settings

---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── requirements.txt
├── prod/
│   ├── manage.py
│   ├── accounts/           # Registration, activation, password reset APIs
│   ├── authentication/     # JWT + JWE + Cookie handling
│   ├── middleware/         # Security middleware
│   ├── tasks/              # Celery tasks
│   ├── prod/               # Core settings (dev + prod)
│   └── ...                 # Other components
```

---

## 📦 Requirements

* Python **3.10+**
* Docker & Docker Compose
* Redis
* RabbitMQ
* PostgreSQL (via Docker)

---

## 🔧 Environment Variables

Create a `.env` file inside `prod/` or root directory:

```
DEBUG=True
SECRET_KEY=your_secret
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=postgres://user:pass@db:5432/dbname

# Security
JWE_KEY=your_jwe_key

# Redis / RabbitMQ
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_pass
DEFAULT_FROM_EMAIL=your_email

# Google Auth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# AWS (optional)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
```

---

## 🐳 Running with Docker (Recommended)

```bash
docker compose up --build -d
```

To stop all services:

```bash
docker compose down
```

---

## 🖥️ Running Locally (Without Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Run Celery
celery -A prod.celery worker --loglevel=info
celery -A prod.celery beat --loglevel=info
```

---

## 🔥 API Endpoints (Summary)

### **Auth**

* POST `/api/auth/login/` — Login (Cookies returned: access + refresh)
* POST `/api/auth/refresh/` — Refresh with token rotation
* POST `/api/auth/logout/` — Logout + Blacklist

### **Account**

* POST `/api/accounts/register/`
* POST `/api/accounts/verify-email/`
* POST `/api/accounts/reset-password/`
* POST `/api/accounts/reset-password-confirm/`

### **Google OAuth2**

* POST `/api/auth/google/`

---

## 🔎 Security Highlights

* **Encrypted JWT (JWE)** → protects token contents even if intercepted
* **HttpOnly Cookies** → JavaScript cannot access tokens
* **SameSite=Strict** → Strong CSRF protection
* **Token Blacklisting & Rotation** → Prevents replay attacks
* Custom middleware for:

  * Suspicious IP change detection
  * Device fingerprint mismatch
  * Session hardening

---

## 📬 Celery Tasks

* Send activation email
* Send password reset email
* Cleanup old blacklisted tokens
* Scheduled tasks with Celery Beat

---

## 🧪 Tests

Available test modules:

* `test_serializers.py`
* `test_views_activation.py`
* `test_views_login.py`
* `test_views_register.py`
* `test_views_reset_password.py`

Run tests:

```bash
python manage.py test
```

---

## 📝 License

Licensed under the **Apache-2.0 License**.

---

## ✨ Author

**Moamen Mahmoud**  — Backend Developer
