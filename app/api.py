from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException
from app.database import engine, SessionLocal
from app.models import Base, Ticket
from app.schemas import TicketCreate, TicketUpdate, TicketAssign

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():

    return {"message": "Support Ticket API"}


@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    db: Session = SessionLocal()

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        category=ticket.category
    )
    db.add(new_ticket)

    db.commit()

    db.refresh(new_ticket)

    db.close()

    return new_ticket


@app.get("/tickets")
def get_tickets():

    db: Session = SessionLocal()

    tickets = db.query(Ticket).all()

    db.close()

    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):

    db: Session = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    db.close()

    return ticket

@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket_update: TicketUpdate):

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

    db.commit()
    db.refresh(ticket)
    db.close()

    return ticket


@app.patch("/tickets/{ticket_id}/assign")
def assign_ticket(ticket_id: int, assignment: TicketAssign):

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
def close_ticket(ticket_id: int):

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