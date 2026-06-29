from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str = "Medium"
    category: str = "Technical"


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    assigned_to: str | None = None
    category: str | None = None
    priority: str | None = None


class TicketAssign(BaseModel):
    assigned_to: str


class TicketClose(BaseModel):
    status: str = "Closed"


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str