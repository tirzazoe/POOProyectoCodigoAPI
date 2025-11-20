from pydantic import BaseModel, Field, field_validator
from typing import Optional
from decimal import Decimal
from datetime import date
import re

class Purchase(BaseModel):
    supplier_id: Optional[int] = Field(
        default=None,
        description="El ID del proveedor al que pertenece el producto"
    )

    code_product: Optional[int] = Field(
        description="Codigo del producto",
        default=None
    )

    purchase_price: Optional[Decimal] = Field(
        description="Precio de venta del producto",
        gt=0,
        default=None
    )

    delivery_date: Optional[date] = Field(
    description="Fecha de entrega del producto",
    default=None
)