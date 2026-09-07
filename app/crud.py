import math

from sqlalchemy.orm import Session

from app import models, schemas


def get_product(db: Session, pid: int):
    return db.query(models.Product).filter(models.Product.id == pid).first()


def get_products_paginated(db: Session, page: int = 1, page_size: int = 10):
    total_records = db.query(models.Product).count()
    total_pages = math.ceil(total_records / page_size) if total_records else 0

    offset = (page - 1) * page_size
    products = (
        db.query(models.Product)
        .order_by(models.Product.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return products, total_records, total_pages


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, pid: int, product: schemas.ProductUpdate):
    db_product = get_product(db, pid)
    if not db_product:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product
