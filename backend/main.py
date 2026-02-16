from fastapi import FastAPI
from database import get_db_connection

from fastapi import HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this right after app = FastAPI()
origins = [
    "http://localhost:5173", # This is where your React app lives
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/expenses")
def read_expenses():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # The SQL Join we wrote earlier!
    cur.execute("""
        SELECT e.description, e.amount_cents / 100.0, c.name 
        FROM expenses e 
        LEFT JOIN categories c ON e.category_id = c.id
    """)
    
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"expenses": data}



# 1. Define what an 'Expense' looks like (Schema)
class ExpenseCreate(BaseModel):
    amount_cents: int
    description: str
    category_id: int = None

@app.post("/expenses")
def create_expense(expense: ExpenseCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "INSERT INTO expenses (amount_cents, description, category_id) VALUES (%s, %s, %s) RETURNING id;",
            (expense.amount_cents, expense.description, expense.category_id)
        )
        new_id = cur.fetchone()[0]
        conn.commit() # Don't forget to commit, or the warehouse won't save it!
        return {"id": new_id, "message": "Expense added successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/overview")
def expensesOverview():
    return {"message" : "new page"}

