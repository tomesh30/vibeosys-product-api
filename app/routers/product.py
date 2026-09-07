from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/list", response_model=schemas.ProductListResponse)
def list_products(
    page: int = Query(1, ge=1, description="Page number, starting at 1"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page"),
    db: Session = Depends(get_db),
):
    """List all products with pagination (default 10 records per page)."""
    products, total_records, total_pages = crud.get_products_paginated(
        db, page=page, page_size=page_size
    )

    return schemas.ProductListResponse(
        pagination=schemas.PaginationMeta(
            total_records=total_records,
            total_pages=total_pages,
            current_page=page,
            page_size=page_size,
        ),
        data=products,
    )


@router.get("/{pid}/info", response_model=schemas.ProductOut)
def get_product_info(pid: int, db: Session = Depends(get_db)):
    """View information about the requested product ID."""
    db_product = crud.get_product(db, pid)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {pid} not found")
    return db_product


@router.post("/add", response_model=schemas.ProductOut, status_code=201)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the database."""
    return crud.create_product(db, product)


@router.put("/{pid}/update", response_model=schemas.ProductOut)
def update_product(pid: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Update an existing product with the given product ID."""
    db_product = crud.update_product(db, pid, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {pid} not found")
    return db_product
