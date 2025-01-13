from pydantic import BaseModel, HttpUrl

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
