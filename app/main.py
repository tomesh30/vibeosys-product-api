from fastapi import FastAPI

from app.database import Base, engine
from app.routers import product

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vibeosys Product API",
    description="A standalone FastAPI application to manage Products (list, info, add, update).",
    version="1.0.0",
)

app.include_router(product.router)


@app.get("/")
def root():
    return {"message": "Vibeosys Product API is running. Visit /docs for Swagger UI."}
