import uvicorn
from fastapi import FastAPI

from lecture_2.hw.shop_api.db import engine, Base
from lecture_2.hw.shop_api.routers.cart_router import cart_router
from lecture_2.hw.shop_api.routers.item_router import item_router

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Shop API")

if __name__ == "__main__":
    app.include_router(cart_router)
    app.include_router(item_router)
    uvicorn.run(app, host="localhost")
