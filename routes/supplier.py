from fastapi import APIRouter, status

from models.supplier import Supplier
from models.purchase import Purchase

from controllers.supplier import (
    create_supplier
    , update_supplier
    ,delete_supplier
    ,get_all
    ,get_one
    ,add_product
    ,get_all_products
    ,get_one_product
    ,remove_product
    ,update_purchase_info
    )

router = APIRouter(prefix="/supplier")

@router.post( "/" , tags=["Supplier"], status_code=status.HTTP_201_CREATED )
async def create_new_supplier(supplier_data: Supplier):
    result = await create_supplier(supplier_data)
    return result

@router.put("/{id_supplier}", tags=["Supplier"], status_code=status.HTTP_201_CREATED)
async def update_supplier_information( supplier_data: Supplier , id_supplier: int ):
    supplier_data.id_supplier = id_supplier
    result = await update_supplier(supplier_data)
    return result

@router.delete("/{id_supplier}", tags=["Supplier"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier_content( id_supplier: int ):
    status: str =  await delete_supplier(id_supplier)
    return status

@router.get( "/" , tags=["Supplier"], status_code=status.HTTP_200_OK )
async def get_all_suppliers():
    result = await get_all()
    return result

@router.get("/{id_supplier}", tags=["Supplier"], status_code=status.HTTP_200_OK)
async def get_one_supplier( id_supplier: int ):
    result: Supplier =  await get_one(id_supplier)
    return result

@router.post("/{id_supplier}/product", tags=["Supplier"], status_code=status.HTTP_201_CREATED)
async def assign_product_to_supplier( id_supplier: int, product_data: Purchase ):
    result = await add_product(id_supplier, product_data.code_product)
    return result

@router.get("/{id_supplier}/product", tags=["Supplier"], status_code=status.HTTP_200_OK)
async def get_all_products_of_supplier( id_supplier: int ):
    result = await get_all_products(id_supplier)
    return result

@router.get("/{id_supplier}/product/{code_product}", tags=["Supplier"], status_code=status.HTTP_200_OK)
async def get_one_product_of_supplier( id_supplier: int, code_product: int ):
    result = await get_one_product(id_supplier, code_product)
    return result

@router.delete("/{id_supplier}/product/{code_product}", tags=["Supplier"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_of_supplier( id_supplier: int, code_product: int ):
    status: str =  await remove_product(id_supplier, code_product)
    return status

@router.put("/{id_supplier}/product/{code_product}", tags=["Supplier"], status_code=status.HTTP_201_CREATED)
async def update_product_of_supplier( id_supplier: int, code_product: int, purchase_data: Purchase ):
    purchase_data.supplier_id = id_supplier
    purchase_data.code_product = code_product
    result = await update_purchase_info(purchase_data)
    return result