import enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    func,
)

from app.database import Base


class CategoryEnum(str, enum.Enum):
    finished = "finished"
    semi_finished = "semi-finished"
    raw = "raw"


class UnitOfMeasureEnum(str, enum.Enum):
    mtr = "mtr"
    mm = "mm"
    ltr = "ltr"
    ml = "ml"
    cm = "cm"
    mg = "mg"
    gm = "gm"
    unit = "unit"
    pack = "pack"


class Product(Base):
    __tablename__ = "products"

    id = Column("product_id", BigInteger, primary_key=True, autoincrement=True)
    name = Column("name", String(100), nullable=False)
    category = Column("category", Enum(CategoryEnum), nullable=False)
    description = Column("description", String(250), nullable=True)
    product_image = Column("product_image", Text, nullable=True)  # URL, varchar(max)
    sku = Column("sku", String(100), nullable=False)
    unit_of_measure = Column("unit_of_measure", Enum(UnitOfMeasureEnum), nullable=False)
    lead_time = Column("lead_time", Integer, nullable=True)  # lead time in days
    created_date = Column("created_date", DateTime, server_default=func.now())
    updated_date = Column(
        "updated_date", DateTime, server_default=func.now(), onupdate=func.now()
    )
