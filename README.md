# High-Level Secure Performance Auth

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Celery](https://img.shields.io/badge/Celery-5.4-orange)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.11-red)
![Redis](https://img.shields.io/badge/Redis-7-orange)

---

## 📌 Overview

A **high-security Django REST Authentication System** designed for production environments with:

* JWT & JWE Authentication (HttpOnly Cookies)
* Email activation + Password reset
* Role-based permissions
* ABAC permissions
* Google OAuth2 login
* Celery async tasks & Celery Beat
* Redis caching
* RabbitMQ message broker
* Clean project architecture ready for scaling

---

## 🚀 Features

* **Secure Registration Flow** with activation email
* **JWT Access/Refresh** stored in HttpOnly cookies (XSS-resistant)
* **Full JWE Encryption** for sensitive payloads
* **Google OAuth2** login & signup
* **Role & Permission System**
* **Asynchronous Emails** via Celery
* **Scheduled Jobs** (cleanup inactive users, clean token blacklist)
* **Redis caching for roles**
* **Fully containerized** with Docker & Docker Compose
* **API rate limiting (throttling)** Authenticated users: 50 requests per minute | Anonymous users: 20 requests per minute




---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── LICENSE
├── rabbitmq.conf
├── README.md
├── prod
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   ├── frontend
│   │   └── try.html
│   ├── common
│   │   ├── pagination.py
│   │   └── permissions.py
│   ├── middleware
│   │   └── decryption_jwe.py
│   ├── managers
│   │   └── user_manager.py
│   ├── authentication
│   │   ├── cookie_jwt.py
│   │   ├── tokens_activate.py
│   │   └── tokens.py
│   ├── accounts
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   ├── authentication_email.py
│   │   ├── api
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   ├── models
│   │   │   ├── role.py
│   │   │   └── user.py
│   │   ├── signals
│   │   │   ├── signals_cache_role.py
│   │   │   └── signals_default_role.py
│   │   ├── tasks
│   │   │   ├── blacklist_jwt_clean.py
│   │   │   ├── in_active_user.py
│   │   │   ├── send_activation_email.py
│   │   │   └── send_reset_password.py
│   │   ├── templates
│   │   │   ├── emails
│   │   │   │   └── activation_email.html
│   │   │   └── reset_password
│   │   │       └── reset_password.html
│   │   └── tests
│   │       ├── test_serializers.py
│   │       ├── test_views_activation.py
│   │       ├── test_views_login.py
│   │       ├── test_views_register.py
│   │       └── test_views_reset_password.py
│   ├── prod
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── settings
│   │       ├── settings_base.py
│   │       ├── settings_dev.py
│   │       └── settings_prod.py
```

---

## 🐳 Docker Setup

### Build & run the full stack

```bash
docker compose up --build -d
```

Services included:

* Django API
* Celery Worker
* Celery Beat
* Redis
* RabbitMQ
* PostgreSQL

To stop:

```bash
docker compose down
```

---

## ⚙️ Environment Variables

Create a `.env` file next to `manage.py`:

```
# Django secret


DEBUG=True

# Allowed hosts
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY = xxxxxx_strong_secret_key_xxxxx
JWE_KEY= xxxx_strong_jwe_key_xxxxx
# Database example
#DB_NAME=your_db_name
#DB_USER=your_db_user
#DB_PASSWORD=your_db_password
#DB_HOST=localhost
#DB_PORT=5432

# Email settings (Gmail example)
EMAIL_HOST_USER=xxxx@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx
DEFAULT_FROM_EMAIL= xxxx@gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST=smtp.gmail.com

# Frontend URL
FRONTEND_URL=http://localhost:8000
GOOGLE_CLIENT_ID = xxxx-xxxx-xxxx-xxxx
GOOGLE_CLIENT_SECRET = xxxx-xxxx-xxx

#Redis_URL
REDIS_URL=redis://127.0.0.1:6379/1

#CELERY_URL (Rabbitmq)
CELERY_BROKER_URL=xxxxxx
CELERY_RESULT_BACKEND=xxxxx

# AWS Storage
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_STORAGE_BUCKET_NAME=xxxx
AWS_S3_REGION_NAME=xxxx

```

---

## 🔐 Authentication Flow

### Registration → Activation

1. User registers
2. Celery sends activation email
3. User clicks activation link
4. Account becomes active

### Login

* Token generated → Stored in secure HttpOnly cookies
* Refresh token rotated securely

### Logout

* Tokens added to blacklist

---

## 🔄 Background & Scheduled Tasks

### Celery Worker handles:

* Sending activation email
* Sending reset password email
* Cleaning inactive accounts
* Cleaning JWT blacklist

### Celery Beat schedules:

* Daily cleanup
* Periodic role-cache refresh

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Includes tests for:

* Serializers
* Authentication flow
* Role and permission handling
* Activation & password reset

---

## 🛡️ Security Highlights

* HttpOnly & Secure cookies
* JWE-encrypted payloads
* CSRF-safe design
* No token exposure to frontend
* Role-based authorization
* Rate-limit friendly architecture

---
## RUN The server by httpS

* openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
* python manage.py runserver_plus 127.0.0.1:8000 --cert-file cert.pem --key-file key.pem


## 📜 License

 Apache License





+-----------------+
|   Frontend      |
+--------+--------+
         |
         v
+-----------------+
|   Django API    |
| JWT & JWE Auth  |
+--------+--------+
         |
         v
+--------+--------+        +----------------+
|   Redis Cache   | <----> | Role-based ACL |
+-----------------+        +----------------+
         |
         v
+--------+--------+
|   Celery Worker |
| async tasks     |
+-----------------+
         |
         v
+--------+--------+
| RabbitMQ Broker |
+-----------------+
         |
         v
+-----------------+
| PostgreSQL DB   |
+-----------------+




