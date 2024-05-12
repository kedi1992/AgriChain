from pydantic import BaseModel


class ItemData(BaseModel):
    item: str
    price: int


class ScanData(BaseModel):
    item: str


class SpecialOfferData(BaseModel):
    item: str
    quantity: int
    specialPrice: int
