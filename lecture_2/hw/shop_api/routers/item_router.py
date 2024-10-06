from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from fastapi.params import Query
from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db import get_db, item_repository
from lecture_2.hw.shop_api.schema import ItemResponse, ItemCreate, ItemUpdate


item_router = APIRouter(prefix="/item")

@item_router.post("", response_model=ItemResponse, status_code=HTTPStatus.CREATED)
def create_item(item_create: ItemCreate, db: Session = Depends(get_db)):
    if item_repository.get_item_by_name(db, item_create.name):
        raise HTTPException(status_code=400, detail=f"Item with name {item_create.name} already exists")
    return item_repository.create_item(db, item_create)


@item_router.get("/{item_id}", response_model=ItemResponse)
def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    item = item_repository.get_item(db, item_id)
    if item is None or item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {item_id} not found")
    return item


@item_router.get("")
def get_item(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        min_price: int = Query(0, ge=0),
        max_price: Optional[int] = Query(None, ge=0),
        show_deleted: bool = Query(False),
        db: Session = Depends(get_db)
):
    if max_price is not None and min_price > max_price:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Wrong params")
    return item_repository.get_item_by_filter(db, offset, limit, min_price, max_price, show_deleted)


@item_router.put("/{item_id}", response_model=ItemResponse)
def put_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    print(item_update)
    item = item_repository.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {item_id} not found")
    if item_update.name is None or item_update.price is None:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Wrong params for put method")
    if item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=f"Item with id {item_id} is deleted")
    return item_repository.update_item(db, item, item_update)


@item_router.patch("/{item_id}", response_model=ItemResponse)
def patch_item(item_id: int, item_update: dict, db: Session = Depends(get_db)):
    if len(item_update) > 0 and item_update.keys() not in [{"price"}, {"name"}, {"price", "name"}]:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Wrong parameters")
    item = item_repository.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {item_id} not found")
    if item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=f"Item with id {item_id} is deleted")
    return item_repository.update_item(db, item, ItemUpdate(name=item_update.get("name"), price=item_update.get("price")))


@item_router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = item_repository.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {item_id} not found")
    item_repository.delete_item(db, item)
