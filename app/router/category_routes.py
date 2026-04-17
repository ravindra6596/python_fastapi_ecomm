from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.constants.strings import ConstStrings
from app.core.event_logger import log_event
from app.core.log_events import LogEvents
from app.database.connection import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services import category_service
from app.schemas.response_schema import CustomResponse
from app.utils.auth_dependency import verify_token
from app.utils.enums import CategorySortField, SortOrder

router = APIRouter(prefix=ConstStrings.CATEGORY_PREFIX, tags=[ConstStrings.CATEGORY_TAG])

@router.post(ConstStrings.GET_POST_ROUTE)
def create_category_route(payload: CategoryCreate, db: Session = Depends(get_db),token_data: dict = Depends(verify_token)):
    try:
        create_category = category_service.create_category_service(db, payload,token_data)

        log_event(
            LogEvents.CATEGORY_CREATED,
            {
                "id": create_category.id,
                "name": create_category.name,
                "created_at": create_category.created_at.isoformat(),
            }
        )
        return CustomResponse.success_response(
            statusCode=201,
            data={},
            message=ConstStrings.CATEGORY_CREATED,
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=CustomResponse.error_response(
                statusCode=e.status_code,
                message=e.detail,
                error=e.detail,
                data={}
            )
        )

@router.get(ConstStrings.GET_POST_ROUTE)
def get_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = Query(None),
    sort_by: CategorySortField = CategorySortField.id,
    order: SortOrder = SortOrder.desc,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    result = category_service.get_category_service(
        db=db,
        page=page,
        limit=limit,
        search=search,
        sort_by=sort_by.value,
        order=order.value,
        token=token_data
    )
    log_event(
        LogEvents.CATEGORY_LISTED,
        {
            "count": len(result),
            "page": page,
            "limit": limit,
            "result": result
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.CATEGORY_FETCHED,
        data=result
    )
# bulk category routes
@router.post(ConstStrings.BULK_CATEGORY_ROUTE)
def create_category_bulk_route(
    payload: List[CategoryCreate],
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    try:
        categories = category_service.create_category_bulk_service(
            db,
            payload,
            token_data
        )

        data =[
            {
                "id": c.id,
                "name": c.name
            }
            for c in categories
        ]
        log_event(
            LogEvents.CATEGORY_BULK_CREATED,
            {
                "count": len(categories),
                "ids": [c.id for c in categories],
                "data": data
            }
        )
        return CustomResponse.success_response(
            statusCode=201,
            message=ConstStrings.MULTI_CATEGORY_CREATED,
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

# Get category by id route
@router.get(ConstStrings.ID_ROUTE)
def get_category_by_id_route(
    id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):

    category = category_service.get_category_by_id_service(db, id, token_data)
    log_event(
        LogEvents.CATEGORY_FETCHED,
        {
            "id": category.id,
            "name": category.name,
            "is_deleted": category.is_deleted,
            "deleted_by": category.deleted_by,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
    )

    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.CATEGORY_FETCHED,
        data=CategoryResponse.model_validate(category),
    )


# update category route
@router.patch(ConstStrings.ID_ROUTE)
def update_category_route(
    id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),token_data: dict = Depends(verify_token)
):
    try:
        updated = category_service.update_category_service(db, id, payload,token_data)
        log_event(
            LogEvents.CATEGORY_UPDATED,
            {
                "id": updated.id,
                "changes": CategoryResponse.model_validate(updated),
            }
        )
        return CustomResponse.success_response(
            statusCode=200,
            message=ConstStrings.CATEGORY_UPDATED,
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

# category delete route
@router.delete(ConstStrings.ID_ROUTE)
def delete_category_route(
    id: int,
    db: Session = Depends(get_db),token_data: dict = Depends(verify_token)
):

    deleted = category_service.delete_category_service(db, id,token_data)
    user_id = token_data.get(ConstStrings.USER_ID_FIELD)
    log_event(
        LogEvents.CATEGORY_DELETED,
        {
            "id": deleted.id,
            "deleted_by": user_id
        }
    )
    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.CATEGORY_DELETED,
        data={}
    )