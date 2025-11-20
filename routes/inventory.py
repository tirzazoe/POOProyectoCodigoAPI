from fastapi import APIRouter, status

from models.inventory import Inventory
from controllers.inventory import (
    create_inventory
    , update_inventory
    , delete_inventory
    , get_all
    ,get_one
    )

router = APIRouter(prefix="/inventory")

@router.post( "/" , tags=["Inventory"], status_code=status.HTTP_201_CREATED )
async def add_product_inventory(inventory_data: Inventory):
    result = await create_inventory(inventory_data)
    return result

@router.put("/{id_inventory}", tags=["Inventory"], status_code=status.HTTP_201_CREATED)
async def update_inventory_information( inventory_data: Inventory , id_inventory: int ):
    inventory_data.id_inventory = id_inventory
    result = await update_inventory(inventory_data)
    return result

@router.delete("/{id_inventory}", tags=["Inventory"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_content( id_inventory: int ):
    status: str =  await delete_inventory(id_inventory)
    return status

@router.get( "/" , tags=["Inventory"], status_code=status.HTTP_200_OK )
async def get_all_inventory():
    result = await get_all()
    return result

@router.get("/{id_inventory}", tags=["Inventory"], status_code=status.HTTP_200_OK)
async def get_one_product_inventory( id_inventory: int ):
    result: Inventory =  await get_one(id_inventory)
    return result
