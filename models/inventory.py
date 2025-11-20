from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
import re

class Inventory(BaseModel):
    id_inventory: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el inventario"
    )

    id_product: Optional[int] = Field(
        description="Codigo del producto",
        default=None
    )

    sale_price: Optional[Decimal] = Field(
        description="Precio de compra del producto",
        gt=0,
        default=None
    )

    quantity: Optional[int] = Field(
    description="Cantidad de productos",
    default=None,
)