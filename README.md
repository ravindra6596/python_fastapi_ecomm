# python_fastapi_ecomm
🛒 FastAPI Mini E-commerce Backend
📌 Overview

A simple backend system built using FastAPI + PostgreSQL to manage products and categories with CRUD operations, filtering, pagination, sorting, and soft delete functionality.

🎯 Objective

Build REST APIs for a mini e-commerce system demonstrating clean backend development, validation, and structured API design.

⚙️ **Tech Stack**
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
  
📦 **Data Models**
- Product -> id, name, description, price, category_id, is_deleted, created_at
- Category -> id, name

🚀 **Features**
**Product APIs**
- Create product
- Get all products
- Get product by ID
- Update product
- Soft delete product
**Category APIs**
- Create category
- Get all categories

🔍 **Functionalities**
- Pagination (page, limit)
- Search by product name
- Filter by category & price range
- Sorting by price & created_at

📊 **Response Format**
- Standard success & error response structure
- Includes total count, page, limit, and items for list APIs
