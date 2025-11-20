from decimal import Decimal
import json
import logging

from fastapi import HTTPException

from models.inventory import Inventory

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_inventory(inventory: Inventory) -> Inventory:
    sqlscript: str = """
    INSERT INTO [sales].[inventory] ([id_product], [sale_price],[quantity] )
    VALUES (?, ?, ?);
    """

    params = [
        inventory.id_product,
        inventory.sale_price,
        inventory.quantity
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sqlfind: str = """
    SELECT [id_product], 
    [sale_price], 
    [quantity]
    FROM [sales].[inventory]
    WHERE id_inventory = ?;
    """

    params = [inventory.id_inventory]

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
    

async def update_inventory( inventory: Inventory ) -> Inventory:

    dict = inventory.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id_inventory')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [sales].[inventory]
        SET {variables}
        WHERE [id_inventory] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( inventory.id_inventory )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    sqlfind: str = """
        SELECT [id_inventory]
            ,[id_product]
            ,[sale_price]
            ,[quantity]
        FROM [sales].[inventory]
        WHERE id_inventory = ?;
    """

    params = [inventory.id_inventory]

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
    
async def delete_inventory( id_inventory: int ) -> str:

    deletescript = """
        DELETE FROM [sales].[inventory]
        WHERE [id_inventory] = ?;
    """

    params = [id_inventory];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_all() -> list[Inventory]:

    selectscript = """
        SELECT [id_inventory]
            ,[id_product]
            ,[sale_price]
            ,[quantity]
        FROM [sales].[inventory]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_one( id_inventory: int ) -> Inventory:

    selectscript = """
        SELECT [id_inventory]
            ,[id_product]
            ,[sale_price]
            ,[quantity]
        FROM [sales].[inventory]
        WHERE id_inventory = ?
    """

    params = [id_inventory]
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
 