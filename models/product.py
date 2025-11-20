from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Product(BaseModel):
    code: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el producto"
    )

    name_product: Optional[str] = Field(
        description="Nombre del producto",
        pattern = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9.,'()°%\- ]+$",
        default=None,
        examples=["Papel Higienico","Crema Humectante"]
    )

    descripcion: Optional[str] = Field(
        description="Descripcion del producto",
        pattern = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9.,'()°%\- ]+$",
        default=None
    )


