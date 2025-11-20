import json
import logging

from fastapi import HTTPException

from models.supplier import Supplier

from models.purchase import Purchase

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_supplier(supplier: Supplier) -> Supplier:
    sqlscript: str = """
    INSERT INTO [sales].[supplier] ([name_supplier], [addresss], [phone])
    VALUES (?, ?, ?);
    """

    params = [
        supplier.name_supplier,
        supplier.addresss,
        supplier.phone
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sqlfind: str = """
    SELECT [id_supplier], 
    [name_supplier], 
    [addresss],
    [phone]
    FROM [sales].[supplier]
    WHERE id_supplier = ?;
    """

    params = [supplier.id_supplier]

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
    
async def update_supplier( supplier: Supplier ) -> Supplier:

    dict = supplier.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id_supplier')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [sales].[supplier]
        SET {variables}
        WHERE [id_supplier] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( supplier.id_supplier )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    sqlfind: str = """
        SELECT [id_supplier]
            ,[name_supplier]
            ,[addresss]
            ,[phone]
        FROM [sales].[supplier]
        WHERE id_supplier = ?;
    """

    params = [supplier.id_supplier]

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
    
async def delete_supplier( id_supplier: int ) -> str:

    deletescript = """
        DELETE FROM [sales].[supplier]
        WHERE [id_supplier] = ?;
    """

    params = [id_supplier];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_all() -> list[Supplier]:

    selectscript = """   
        SELECT [id_supplier]
            ,[name_supplier]
            ,[addresss]
            ,[phone]   
        FROM [sales].[supplier]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_one( id_supplier: int ) -> Supplier:

    selectscript = """
        SELECT [id_supplier]
            ,[name_supplier]
            ,[addresss]
            ,[phone]
        FROM [sales].[supplier]
        WHERE id_supplier = ?
    """

    params = [id_supplier]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"supplier not found")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def add_product(supplier_id: int, code_product: int, purchase : Purchase) -> Purchase:

    insert_script = """
        INSERT INTO [sales].[purchase] ([supplier_id], [code_product], [purchase_price], [delivery_date])
        VALUES (?, ?, ?, ?);
    """

    params = [
        supplier_id,
        code_product,
        purchase.purchase_price,
        purchase.delivery_date
    ]

    try:
        await execute_query_json(insert_script, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            pp.code_product
            , p.name_product
            , s.name_supplier
            , pp.purchase_price
            , pp.delivery_date
        FROM sales.purchase pp
        inner join sales.product p
        on pp.code_product = p.code
        WHERE pp.supplier_id = ?
        and pp.code_product = ?;
    """

    params = [supplier_id, code_product]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def get_all_products(supplier_id: int) -> list[Purchase]:
    select_script = """
        SELECT
            pp.code_product
            , p.name_product
            , s.name_supplier
            , pp.purchase_price
            , pp.delivery_date
        FROM sales.purchase pp
        inner join sales.product p
        on pp.code_product = p.code
        WHERE pp.supplier_id = ?
    """

    params = [supplier_id]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No products were found for this supplier")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def get_one_product(supplier_id: int, code_product: int) -> Purchase:
    select_script = """
        SELECT
             pp.code_product
            , p.name_product
            , s.name_supplier
            , pp.purchase_price
            , pp.delivery_date
        FROM sales.purchase pp
        inner join sales.product p
        on pp.code_product = p.code
        WHERE pp.supplier_id = ?
        and pp.code_product = ?;
    """

    params = [supplier_id, code_product]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No product found for this supplier")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def remove_product(supplier_id: int, code_product: int) -> str:
    delete_script = """
        DELETE FROM [sales].[purchase]
        WHERE [supplier_id] = ? AND [code_product] = ?;
    """

    params = [supplier_id, code_product]

    try:
        await execute_query_json(delete_script, params=params, needs_commit=True)
        return "PRODUCT REMOVED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

async def update_purchase_info(purchase_data: Purchase) -> Purchase:
    dict = purchase_data.model_dump(exclude_none=True)
    keys = [ k for k in  dict.keys() ]
    keys.remove('supplier_id')
    keys.remove('code_product')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [sales].[purchase]
        SET {variables}
        WHERE [supplier_id] = ? AND [code_product] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( purchase_data.supplier_id )
    params.append( purchase_data.code_product )

    try:
        await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
             pp.code_product
            , p.name_product
            , s.name_supplier
            , pp.purchase_price
            , pp.delivery_date
        FROM sales.purchase pp
        inner join sales.product p
        on pp.code_product = p.code
        WHERE pp.supplier_id = ?
        and pp.code_product = ?;
    """

    params = [purchase_data.supplier_id, purchase_data.code_product]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")