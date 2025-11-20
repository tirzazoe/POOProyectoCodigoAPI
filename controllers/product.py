import json
import logging

from fastapi import HTTPException

from models.product import Product

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_product(product: Product) -> Product:
    sqlscript: str = """
    INSERT INTO [sales].[product] ([name_product], [descripcion])
    VALUES (?, ?);
    """

    params = [
        product.name_product,
        product.descripcion
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sqlfind: str = """
    SELECT [code], 
    [name_product], 
    [descripcion]
    FROM [sales].[product]
    WHERE code = ?;
    """

    params = [product.code]

    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def update_product( product: Product ) -> Product:

    dict = product.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('code')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [sales].[product]
        SET {variables}
        WHERE [code] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( product.code )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    sqlfind: str = """
        SELECT [code]
            ,[name_product]
            ,[descripcion]
        FROM [sales].[product]
        WHERE code = ?;
    """

    params = [product.code]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    

async def delete_product( code: int ) -> str:

    deletescript = """
        DELETE FROM [sales].[product]
        WHERE [code] = ?;
    """

    params = [code];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_all() -> list[Product]:

    selectscript = """
        SELECT [code]
            ,[name_product]
            ,[descripcion]
        FROM [sales].[product]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_one( code: int ) -> Product:

    selectscript = """
        SELECT [code]
            ,[name_product]
            ,[descripcion]
        FROM [sales].[product]
        WHERE code = ?
    """

    params = [code]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"product not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")










