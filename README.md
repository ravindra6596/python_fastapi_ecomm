# python_fastapi_ecomm
🛒 FastAPI Mini E-commerce Backend

📌 Overview
A backend system built using FastAPI + PostgreSQL to manage products and categories with CRUD operations, filtering, pagination, sorting, soft delete, and JWT authentication.

🎯 Objective
Build REST APIs for a mini e-commerce system demonstrating clean backend development, authentication, and structured API design.

⚙️ Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication

📦 Data Models
- Product -> id, name, description, price, category_id, is_deleted, created_at, updated_at
- Category -> id, name, is_deleted
- User -> id, name, email, password (hashed)

🔐 Authentication Features
- User Register
- User Login (JWT Access + Refresh Token)
- Refresh Token
- Logout

🚀 Features

**Product APIs**
- Create product
- Get all products
- Get product by ID
- Update product
- Soft delete product

**Category APIs**
- Create category
- Get all categories
- Soft delete category (cascade to products)

🔍 Functionalities
- Pagination (page, limit)
- Search by product name & category name
- Filter by category & price range
- Sorting by price & created_at
- JWT protected routes

📊 Response Format
- Standard success & error response structure
- Includes total count, page, limit, and items for list APIs

🧠 Key Features Implemented
JWT Authentication system
Role-based structure ready
Soft delete for safety
Cascade delete (category → products)
Search across multiple fields
Pagination + sorting
Clean architecture (service/repository pattern)

📌 Future Improvements
Role-based access control (RBAC)
Redis for token blacklisting
Docker setup
Unit tests (pytest)
API documentation enhancements
