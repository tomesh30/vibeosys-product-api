from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import CategoryEnum, UnitOfMeasureEnum


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: CategoryEnum
    description: Optional[str] = Field(None, max_length=250)
    product_image: Optional[str] = Field(None, description="Image URL")
    sku: str = Field(..., max_length=100)
    unit_of_measure: UnitOfMeasureEnum
    lead_time: Optional[int] = Field(None, ge=0, le=999, description="Lead time in days")


class ProductCreate(ProductBase):
    """Schema used for POST /product/add"""
    pass


class ProductUpdate(BaseModel):
    """Schema used for PUT /product/{pid}/update - all fields optional (partial update)."""
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[CategoryEnum] = None
    description: Optional[str] = Field(None, max_length=250)
    product_image: Optional[str] = None
    sku: Optional[str] = Field(None, max_length=100)
    unit_of_measure: Optional[UnitOfMeasureEnum] = None
    lead_time: Optional[int] = Field(None, ge=0, le=999)


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_date: datetime
    updated_date: datetime


class PaginationMeta(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    page_size: int


class ProductListResponse(BaseModel):
    pagination: PaginationMeta
    data: List[ProductOut]
