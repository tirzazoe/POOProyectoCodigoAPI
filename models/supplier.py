from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Supplier(BaseModel):
    id_supplier: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el proveedor"
    )

    name_supplier: Optional[str] = Field(
        description="Nombre del proveedor",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["UNILEVER","Distribuidora El Milagro"]
    )

    addresss: Optional[str] = Field(
        description="Direccion del proveedor",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9#°.,' -]+$",
        default=None,
        examples=["Colonia Santa Rosa, calle 6"]
    )

    phone: Optional[str] = Field(
    description="Teléfono del proveedor",
    pattern=r"^\+?[0-9]{1,3}?[0-9 ()-]{7,20}$",
    default=None,
    examples= ["+504 87540976","9656 8943"]
)