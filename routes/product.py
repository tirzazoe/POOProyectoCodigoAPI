from fastapi import APIRouter, status

from models.product import Product
from controllers.product import (
    create_product
    , update_product
    , delete_product
    , get_all
    , get_one
    )

router = APIRouter(prefix="/product")

@router.post( "/" , tags=["Product"], status_code=status.HTTP_201_CREATED )
async def create_new_product(product_data: Product):
    result = await create_product(product_data)
    return result

@router.put("/{code}", tags=["Product"], status_code=status.HTTP_201_CREATED)
async def update_product_information( product_data: Product , code: int ):
    product_data.code = code
    result = await update_product(product_data)
    return result

@router.delete("/{code}", tags=["Product"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_content( code: int ):
    status: str =  await delete_product(code)
    return status

@router.get( "/" , tags=["Product"], status_code=status.HTTP_200_OK )
async def get_all_products():
    result = await get_all()
    return result

@router.get("/{code}", tags=["Product"], status_code=status.HTTP_200_OK)
async def get_one_product( code: int ):
    result: Product =  await get_one(code)
    return result