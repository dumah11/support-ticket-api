from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()


class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    status = Column(String, default="Open")

    assigned_to = Column(String, default="")

    
    category = Column(String, default="Technical")

    priority = Column(String, default="Medium")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

