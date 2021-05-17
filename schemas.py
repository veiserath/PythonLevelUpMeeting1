from pydantic import BaseModel
from typing import Optional
from utils import CaseMixin


class ConfiguredBaseModel(BaseModel):
    """Generic schema with configuration for all schemas."""

    class Config:
        orm_mode = True
        alias_generator = CaseMixin.to_pascal


class SupplierBrief(ConfiguredBaseModel):
    """Supplier schema with less information for all suppliers view."""
    supplier_id: Optional[int]
    company_name: str


class Supplier(SupplierBrief):
    """Supplier schema for detailed view."""
    contact_name: Optional[str]
    contact_title: Optional[str]
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    fax: Optional[str]
    homepage: Optional[str]


class SupplierUpdate(Supplier):
    """Supplier schema for updating record."""
    company_name: Optional[str]


class Category(ConfiguredBaseModel):
    """Category schema for products list view."""
    category_id: int
    category_name: str


class Product(ConfiguredBaseModel):
    """Product schema for list view."""
    product_id: int
    product_name: str
    category: Optional[Category]
    discontinued: int
