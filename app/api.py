from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base, Ticket, User
from app.schemas import TicketCreate, TicketUpdate, TicketAssign, UserCreate, Token
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_db,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support Ticket API")


@app.get("/")
def home():
    return {"message": "Support Ticket API"}


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
    }


@app.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.post("/tickets")
def create_ticket(
    ticket: TicketCreate,
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    db.close()

    return new_ticket


@app.get("/tickets")
def get_tickets(
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    tickets = db.query(Ticket).all()

    db.close()

    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    db.close()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@app.put("/tickets/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        db.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket_update.title is not None:
        ticket.title = ticket_update.title

    if ticket_update.description is not None:
        ticket.description = ticket_update.description

    if ticket_update.status is not None:
        ticket.status = ticket_update.status

    if ticket_update.assigned_to is not None:
        ticket.assigned_to = ticket_update.assigned_to

    if ticket_update.category is not None:
        ticket.category = ticket_update.category

    if ticket_update.priority is not None:
        ticket.priority = ticket_update.priority

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket


@app.patch("/tickets/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    assignment: TicketAssign,
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        db.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.assigned_to = assignment.assigned_to

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket


@app.patch("/tickets/{ticket_id}/close")
def close_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
):
    db: Session = SessionLocal()

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket is None:
        db.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = "Closed"

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket