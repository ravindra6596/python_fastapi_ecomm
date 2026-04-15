from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.connection import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.services import category_service
from app.schemas.response_schema import CustomResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
def create_category_route(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        create_category = category_service.create_category_service(db, payload)
        category_data = CategoryResponse.model_validate(
            create_category
        )
        return CustomResponse.success_response(
            statusCode=201,
            data=category_data,
            message="Category created successfully"
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=CustomResponse.error_response(
                statusCode=e.status_code,
                message=e.detail,
                error=e,
                data={}
            )
        )

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
        category_data = category_service.get_category_service(db)

        return CustomResponse.success_response(
            statusCode=200,
            message="Categories fetched successfully",
            data=category_data
        )
