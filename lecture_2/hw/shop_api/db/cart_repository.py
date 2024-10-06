from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db.models import Cart, ItemCart


def create_cart(db: Session):
    cart = Cart()
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart.id

def get_cart_by_id(db: Session, cart_id: int):
    return db.get(Cart, cart_id)

def get_cart(db: Session, cart_id: int):
    return db.query(ItemCart).filter_by(cart_id=cart_id).all()

def add_item_to_cart(db: Session, cart_id: int, item_id: int):
    item_cart = db.query(ItemCart).filter_by(cart_id=cart_id, item_id=item_id).first()
    if item_cart is not None:
        item_cart.quantity += 1
        db.commit()
    else:
        item_cart = ItemCart(cart_id=cart_id, item_id=item_id, quantity=1)
        db.add(item_cart)
        db.commit()

def get_cart_by_filter(db: Session,
    offset: int = 0,
    limit: int = 10,
    min_price: float = 0,
    max_price: float = None,
    min_quantity: float = 0,
    max_quantity: float = None,
):
    carts = db.query(Cart).all()
    carts = [(
        cart.id,
        sum([elem.quantity for elem in cart.cart_items]),
        sum([elem.item_relation.price for elem in cart.cart_items])
    ) for cart in carts]

    if max_quantity is None and max_price is None:
        carts = list(filter(lambda x: x[2] >= min_price and x[1] >= min_quantity, carts))
    elif max_price is None:
        carts = list(filter(lambda x: x[2] >= min_price and max_quantity >= x[1] >= min_quantity, carts))
    elif max_quantity is None:
        carts = list(filter(lambda x: max_price >= x[2] >= min_price and x[1] >= min_quantity, carts))
    else:
        carts = list(filter(lambda x: max_price >= x[2] >= min_price and max_quantity >= x[1] >= min_quantity, carts))

    begin_index = min(len(carts), offset)
    end_index = min(len(carts), offset + limit)

    return [cart[0] for cart in carts[begin_index:end_index]]
