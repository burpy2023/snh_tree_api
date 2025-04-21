from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from typing import List  # make sure this is at the top

from models import TreeNode, TreeNodeCreate, TreeNodeRead
from database import engine, create_db_and_tables
import crud

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/api/tree", response_model=List[TreeNodeRead])
def get_tree():
    with Session(engine) as session:
        return crud.get_full_tree(session)

@app.post("/api/tree", response_model=TreeNodeRead)
def create_node(data: TreeNodeCreate):
    with Session(engine) as session:
        return crud.create_node(session, data)
