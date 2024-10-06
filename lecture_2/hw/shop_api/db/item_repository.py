from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db.models import Item
from lecture_2.hw.shop_api.schema import ItemUpdate, ItemCreate


def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.get(Item, item_id)

def get_item_by_name(db: Session, name: str):
    return db.query(Item).filter_by(name=name).first()

def get_item_by_filter(
        db: Session,
        offset: int = 0,
        limit: int = 10,
        min_price: float = 0,
        max_price: float = None,
        show_deleted: bool = False
):
    if max_price is None and show_deleted:
        return db.query(Item).filter(Item.price >= min_price).limit(limit).offset(offset).all()
    if max_price is None:
        return db.query(Item).filter((Item.price >= min_price) & (Item.deleted == False)).limit(limit).offset(offset).all()
    if show_deleted:
        return db.query(Item).filter(
            (Item.price >= min_price) & (Item.price <= max_price)).limit(limit).offset(offset).all()
    return db.query(Item).filter(
        (Item.price >= min_price) & (Item.deleted == False) & (Item.price <= max_price)
    ).limit(limit).offset(offset).all()

def update_item(db: Session, item: Item, item_update: ItemUpdate):
    if item_update.name is not None:
        item.name = item_update.name
    if item_update.price is not None:
        item.price = item_update.price
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item: Item):
    item.deleted = True
    db.commit()
    db.refresh(item)
