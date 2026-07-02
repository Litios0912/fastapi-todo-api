#!/usr/bin/env python3
"""
FastAPI Todo API
CRUD completo de tareas con autenticacion, SQLite y documentacion Swagger automatica.
Uso: uvicorn main:app --reload
"""

from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="Todo API",
    description="API REST de tareas con autenticacion basica, CRUD completo y documentacion automatica.",
    version="1.0.0",
)
security = HTTPBasic()

USERS = {
    "admin": "admin123",
    "user": "user123",
}


class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), default="")
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class TodoCreate(BaseModel):
    title: str
    description: str = ""


class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None


class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    pwd = USERS.get(credentials.username)
    if not pwd or pwd != credentials.password:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    return credentials.username


@app.get("/")
def root():
    return {"message": "Todo API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/todos", response_model=TodoOut, status_code=201, tags=["Todos"])
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), user: str = Depends(auth)):
    item = TodoDB(title=todo.title, description=todo.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/todos", response_model=list[TodoOut], tags=["Todos"])
def list_todos(completed: bool = None, db: Session = Depends(get_db), user: str = Depends(auth)):
    query = db.query(TodoDB)
    if completed is not None:
        query = query.filter(TodoDB.completed == completed)
    return query.all()


@app.get("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"])
def get_todo(todo_id: int, db: Session = Depends(get_db), user: str = Depends(auth)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo no encontrado")
    return item


@app.put("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"])
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db), user: str = Depends(auth)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo no encontrado")
    if todo.title is not None:
        item.title = todo.title
    if todo.description is not None:
        item.description = todo.description
    if todo.completed is not None:
        item.completed = todo.completed
    db.commit()
    db.refresh(item)
    return item


@app.delete("/todos/{todo_id}", status_code=204, tags=["Todos"])
def delete_todo(todo_id: int, db: Session = Depends(get_db), user: str = Depends(auth)):
    item = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Todo no encontrado")
    db.delete(item)
    db.commit()
