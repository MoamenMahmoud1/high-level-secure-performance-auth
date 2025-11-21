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

Create a `.env` file next to `docker-compose.yml`:

```
SECRET_KEY=your_secret_key
DEBUG=False
POSTGRES_DB=prod_db
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=strongpass
POSTGRES_HOST=postgres
REDIS_HOST=redis
RABBIT_HOST=rabbitmq
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_pass
GOOGLE_CLIENT_ID=xxxxx
GOOGLE_CLIENT_SECRET=xxxxx
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

## 📜 License

MIT License

---

If you want, I can add:
✅ API Documentation section
✅ Sequence diagrams
✅ Service architecture diagrams
✅ Full Docker architecture image

Just tell me and I'll add them.
