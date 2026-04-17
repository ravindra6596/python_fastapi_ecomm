from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.exception.global_exception import global_exception_handler, http_exception_handler, \
    validation_exception_handler
from app.router import auth_routes, category_routes, products_route
app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router) # Auth routes
app.include_router(category_routes.router) # category routes
app.include_router(products_route.router) # products routes

Base.metadata.create_all(bind=engine)
