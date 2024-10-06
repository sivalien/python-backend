from sqlalchemy import Integer, Column, String, Double, Boolean, ForeignKey
from sqlalchemy.orm import relationship, MappedColumn

from . import Base

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    item_carts = relationship("ItemCart", back_populates="item_relation")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    cart_items = relationship("ItemCart", back_populates="cart_relation")

class ItemCart(Base):
    __tablename__ = "item_cart"

    id = Column(Integer, primary_key=True)
    cart_id = MappedColumn(Integer, ForeignKey("cart.id"))
    item_id = MappedColumn(Integer, ForeignKey("item.id"))
    quantity = Column(Integer, nullable=False)

    cart_relation = relationship("Cart", back_populates="cart_items")
    item_relation = relationship("Item", back_populates="item_carts")
