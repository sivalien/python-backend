from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException, Query, APIRouter
from starlette.responses import Response

from lecture_2.hw.shop_api.db import get_db, cart_repository, item_repository
from lecture_2.hw.shop_api.schema import ItemCreatedResponse, CartResponse, ItemCartResponse

cart_router = APIRouter(prefix="/cart")

@cart_router.post("", status_code=HTTPStatus.CREATED, response_model=ItemCreatedResponse)
def post_cart(response: Response, db = Depends(get_db)):
    cart_id = cart_repository.create_cart(db)
    response.headers["Location"] = f"/cart/{cart_id}"
    return ItemCreatedResponse(id=cart_id)


@cart_router.get("/{cart_id}")
def get_cart(cart_id: int, db = Depends(get_db)):
    cart = cart_repository.get_cart_by_id(db, cart_id)
    if cart is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Cart with id {cart_id} not found")
    print(f"cart_id {cart_id}")
    return get_cart_internal(db, cart_id)


def get_cart_internal(db, cart_id):
    items = cart_repository.get_cart(db, cart_id)
    price = sum(map(lambda item_cart: item_cart.quantity * item_cart.item_relation.price, items))
    return CartResponse(
        id=cart_id,
        items=list(map(lambda item_cart: ItemCartResponse(
            id=item_cart.item_id,
            name=item_cart.item_relation.name,
            quantity=item_cart.quantity,
            available=not item_cart.item_relation.deleted
        ), items)),
        price=price
    )

@cart_router.get("")
def get_cart_by_filter(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: int = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    min_quantity: int = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
    db = Depends(get_db)
):
    carts = cart_repository.get_cart_by_filter(
        db,
        offset,
        limit,
        0 if min_price is None else min_price,
        max_price,
        0 if min_quantity is None else min_quantity,
        max_quantity
    )

    return [get_cart_internal(db, cart_id) for cart_id in carts]

@cart_router.post("/{cart_id}/add/{item_id}")
def post_cart(cart_id: int, item_id: int, db = Depends(get_db)):
    print("call add item endpoint")
    if cart_repository.get_cart_by_id(db, cart_id) is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Cart with id {cart_id} not found")
    if item_repository.get_item(db, item_id) is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Item with id {item_id} not found")
    cart_repository.add_item_to_cart(db, cart_id, item_id)
    print(f"Added item {item_id} to cart {cart_id} got {len(cart_repository.get_cart(db, cart_id))} elements")
