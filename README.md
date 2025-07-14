# 🏷️ Inventory System

A web-based inventory management system built with Django and REST Framework, designed to handle products with multiple variants and provide insightful stock analysis — including purchase and sale tracking per variant.

---

## ✨ Features

- 📦 **Product & Variant Management** – Add products with multiple variants (e.g., size, color).
- 📊 **Stock Reports** – Track purchase and sale data for each product variant.
- 🔒 **Authentication** – Secure login with token-based authentication using Simple JWT.
- 🔍 **Filtering & Search** – Easily filter with dates and stock change type (purchase/sale) with `django-filter`.
- 📮 **OTP System** – Email OTP verification for Authentication used upstash to store OTP
- 🛢️ **PostgreSQL + Supabase** – Used supabase for storing in a live db

---

## 🧰 Tech Stack

| Technology     | Purpose                          |
|----------------|----------------------------------|
| **Django**     | Web framework                    |
| **Django REST Framework** | REST API creation        |
| **Simple JWT** | Token-based authentication       |
| **PostgreSQL** | Relational database (via Supabase) |
| **Redis** (Upstash) | Store OTPs |
| **django-filter** | Query filtering for DRF APIs   |

---

