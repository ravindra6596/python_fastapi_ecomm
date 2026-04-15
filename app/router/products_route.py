from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.connection import get_db
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service
from app.utils.enums import ProductSortField, SortOrder
from app.schemas.response_schema import CustomResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("")
def create_products_route(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        create_products = product_service.create_product_service(db, payload)
        products_data = ProductResponse.model_validate(
            create_products
        )
        return CustomResponse.success_response(
            statusCode=201,
            message="Product created successfully",
            data=products_data,
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=CustomResponse.error_response(
                statusCode=e.status_code,
                message=e.detail,
                error=str(e),
                data={}
            )
        )

@router.get("", response_model=dict)
def get_products_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: ProductSortField = ProductSortField.id,
    order: SortOrder = SortOrder.desc,

    db: Session = Depends(get_db)
):

    result = product_service.get_products_service(
        db=db,
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        order=order
    )

    return CustomResponse.success_response(
        statusCode=200,
        message="Products fetched successfully",
        data=result
    )


# Get product by id route
@router.get("/{id}")
def get_product_by_id( id: int, db: Session = Depends(get_db)):
    result = product_service.get_product_by_id(db,  id)
    if not result:
        return CustomResponse.error_response(
            statusCode=404,
            error=None,
            message="Product not found",
            data={}
    )

    return CustomResponse.success_response(
        statusCode=200,
        message="Product Fetched successfully",
        data=ProductResponse.model_validate(result)
    )


# Update product route
@router.patch("/{id}" )
def update_product_route(
        id: int,
        product: ProductUpdate,
        db: Session = Depends(get_db),
):


    updated_product = (
        product_service.update_product_service(db, id, product)
    )

    if not updated_product:
        return CustomResponse.error_response(
            statusCode=404,
            message="Product not found",
            error=None,
            data={}
        )

    return CustomResponse.success_response(
        statusCode=200,
        message="Product updated successfully",
        data=ProductResponse.model_validate(
            updated_product
        )
    )

@router.delete("/{id}")
def soft_delete_product_route(
     id: int,
    db: Session = Depends(get_db)
):

    deleted_product = product_service.soft_delete_product_service(
        db,
        id
    )

    return CustomResponse.success_response(
        statusCode=200,
        message="Product deleted successfully",
        data=ProductResponse.model_validate(deleted_product)
    )