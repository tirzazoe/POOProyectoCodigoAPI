import uvicorn
import os
from typing import Union
from fastapi import FastAPI
from routes.product import router as router_product
from routes.inventory import router as router_inventory
from routes.supplier import router as router_supplier

app = FastAPI()

app.include_router(router_product)

app.include_router(router_inventory)

app.include_router(router_supplier)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")