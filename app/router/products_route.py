from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.constants.strings import ConstStrings
from app.core.event_logger import log_event
from app.core.log_events import LogEvents
from app.database.connection import get_db
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service
from app.utils.auth_dependency import verify_token
from app.utils.enums import ProductSortField, SortOrder
from app.schemas.response_schema import CustomResponse

router = APIRouter(prefix=ConstStrings.PRODUCT_PREFIX, tags=[ConstStrings.PRODUCT_TAG])


@router.post(ConstStrings.GET_POST_ROUTE)
def create_products_route(payload: ProductCreate, db: Session = Depends(get_db),token_data: dict = Depends(verify_token)):
    try:
        create_products = product_service.create_product_service(db, payload, token_data)
        product = ProductResponse.model_validate(
            create_products
        )
        log_event(
            LogEvents.PRODUCT_CREATED,
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "category_id": product.category_id,
                "description": product.description,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
            }
        )
        return CustomResponse.success_response(
            statusCode=201,
            message=ConstStrings.PRODUCT_CREATED,
            data={},
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

@router.get(ConstStrings.GET_POST_ROUTE, response_model=dict)
def get_products_route(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = None,
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: ProductSortField = ProductSortField.id,
    order: SortOrder = SortOrder.desc,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
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
        order=order,
        token=token_data
    )
    log_event(
        LogEvents.PRODUCT_LISTED,
        {
            "count": len(result),
            "page": page,
            "limit": limit,
            "filters": {
                "search": search,
                "category_id": category_id
            },
            "result": result
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.PRODUCTS_FETCHED,
        data=result
    )


# Get product by id route
@router.get(ConstStrings.ID_ROUTE)
def get_product_by_id( id: int, db: Session = Depends(get_db),token_data: dict = Depends(verify_token)):
    result = product_service.get_product_by_id(db,  id,token_data)
    if not result:
        return CustomResponse.error_response(
            statusCode=404,
            error=None,
            message=ConstStrings.NO_PRODUCT,
            data={}
    )
    log_event(
        LogEvents.PRODUCT_FETCHED,
        {
            "id": result.id,
            "name": result.name,
            "is_deleted": result.is_deleted,
            "deleted_by": result.deleted_by,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.PRODUCTS_FETCHED,
        data=ProductResponse.model_validate(result)
    )


# Update product route
@router.patch(ConstStrings.ID_ROUTE)
def update_product_route(
        id: int,
        product: ProductUpdate,
        db: Session = Depends(get_db),token_data: dict = Depends(verify_token)
):


    updated_product = (
        product_service.update_product_service(db, id, product, token_data)
    )

    if not updated_product:
        return CustomResponse.error_response(
            statusCode=404,
            message=ConstStrings.NO_PRODUCT,
            error=None,
            data={}
        )
    log_event(
        LogEvents.PRODUCT_UPDATED,
        {
            "id": updated_product.id,
            "changes": ProductResponse.model_validate(updated_product),
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.PRODUCT_UPDATED,
        data={}
    )

@router.delete(ConstStrings.ID_ROUTE)
def soft_delete_product_route(
    id: int,
    db: Session = Depends(get_db),token_data: dict = Depends(verify_token)
):

    deleted_product = product_service.soft_delete_product_service(
        db,
        id,token_data
    )
    log_event(
        LogEvents.PRODUCT_DELETED,
        {
            "id": deleted_product.id,
            "changes": ProductResponse.model_validate(deleted_product),
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.PRODUCT_DELETED,
        data={}
    )

@router.post(ConstStrings.BULK_PRODUCT_ROUTE)
def create_products_bulk(
    payload: List[ProductCreate],
    db: Session = Depends(get_db),
        token_data: dict = Depends(verify_token)
):
    try:
        products = product_service.create_products_bulk_service(db, payload, token_data)

        data = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "category_id": p.category_id,
                "created_at": p.created_at,
                "updated_at": p.updated_at
            }
            for p in products
        ]
        log_event(
            LogEvents.PRODUCT_BULK_CREATED,
            {
                "count": len(products),
                "ids": [c.id for c in products],
                "data": data
            }
        )
        return CustomResponse.success_response(
            statusCode=201,
            message=ConstStrings.MULTI_PRODUCTS_CREATED,
            data={}
        )

    except HTTPException as e:
        return CustomResponse.error_response(
            statusCode=e.status_code,
            message=e.detail,
            error=str(e),
            data={}
        )

    except Exception as e:
        return CustomResponse.error_response(
            statusCode=500,
            message=ConstStrings.INTERNAL_SERVER_ERROR,
            error=str(e),
            data={}
        )