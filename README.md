# Vibeosys Assignment – Python FastAPI (Product APIs)

A standalone FastAPI application implementing 4 REST APIs for a `Product` entity,
backed by MySQL via SQLAlchemy ORM, with request/response validation via Pydantic.

## Tech Stack
- Python 3.11+
- FastAPI
- Pydantic (validation)
- SQLAlchemy (ORM)
- MySQL (database) + PyMySQL (driver)

## Project Structure
```
vibeosys_product_api/
├── app/
│   ├── main.py            # FastAPI app entry point, creates DB tables on startup
│   ├── database.py        # DB engine/session setup (reads config from .env)
│   ├── models.py          # SQLAlchemy Product model + enums
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── crud.py            # DB access functions (list/get/create/update)
│   └── routers/
│       └── product.py     # 4 API endpoints
├── requirements.txt
├── .env.example            # Sample DB config - copy to .env
├── .gitignore
└── README.md
```

## APIs Implemented
| Method | Endpoint                | Description                                   |
|--------|--------------------------|------------------------------------------------|
| GET    | `/product/list`          | List all products, paginated (10/page default) |
| GET    | `/product/{pid}/info`    | View a single product's info                    |
| POST   | `/product/add`           | Add a new product                               |
| PUT    | `/product/{pid}/update`  | Update an existing product                      |

Interactive Swagger docs are auto-generated at `/docs` once the app is running.

## Database Table: `products`
| Column           | Type                                                                 |
|------------------|-----------------------------------------------------------------------|
| product_id       | BIGINT, Primary Key, Auto Increment                                   |
| name             | VARCHAR(100)                                                          |
| category         | ENUM('finished', 'semi-finished', 'raw')                              |
| description      | VARCHAR(250)                                                          |
| product_image    | TEXT (stores an image URL, unbounded length)                          |
| sku              | VARCHAR(100)                                                          |
| unit_of_measure  | ENUM('mtr','mm','ltr','ml','cm','mg','gm','unit','pack')              |
| lead_time        | INT (lead time in days)                                               |
| created_date     | TIMESTAMP (auto-set on insert)                                        |
| updated_date     | TIMESTAMP (auto-set on insert and update)                             |

The table is created automatically on first run (`Base.metadata.create_all`), so
no manual `CREATE TABLE` script is required — you only need to create the empty
database (schema) itself in MySQL.

## Setup & Run Instructions (Local)

### 1. Prerequisites
- Python 3.11 or higher installed
- MySQL Server installed and running

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database
Log into MySQL and run:
```sql
CREATE DATABASE vibeosys_db;
```

### 5. Configure environment variables
Copy `.env.example` to `.env` and update with your MySQL credentials:
```bash
cp .env.example .env
```
```
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=vibeosys_db
```

### 6. Run the application
```bash
uvicorn app.main:app --reload
```
The app will start at: `http://127.0.0.1:8000`
The `products` table is auto-created on startup.

### 7. Test the APIs
Open Swagger UI in your browser: `http://127.0.0.1:8000/docs`

Or via curl:
```bash
# Add a product
curl -X POST http://127.0.0.1:8000/product/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Steel Rod","category":"raw","description":"10mm steel rod","product_image":"http://example.com/img.jpg","sku":"SKU-001","unit_of_measure":"mtr","lead_time":5}'

# List products (page 1, 10 per page)
curl "http://127.0.0.1:8000/product/list?page=1&page_size=10"

# Get product info
curl http://127.0.0.1:8000/product/1/info

# Update a product
curl -X PUT http://127.0.0.1:8000/product/1/update \
  -H "Content-Type: application/json" \
  -d '{"lead_time":10}'
```

## Notes
- This is a fully standalone application — it does not call any external/internet APIs.
- Partial updates are supported on `/product/{pid}/update` (send only the fields you want to change).
- Pagination defaults to 10 records per page; `page` and `page_size` query params can be adjusted (max `page_size` is 100).
