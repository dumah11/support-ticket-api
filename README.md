# Support Ticket Management System

## Overview

A backend support ticket management platform built using FastAPI, SQLAlchemy, SQLite and Streamlit.

The application allows users to create, manage, assign and close support tickets while providing operational metrics through a dashboard interface.

## Features

* Create support tickets
* View all tickets
* View ticket by ID
* Update ticket details
* Assign tickets to support agents
* Close tickets
* Ticket priorities
* Ticket categories
* Ticket creation timestamps
* Dashboard analytics
* Docker deployment support

## Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Streamlit
* Docker
* Git

## API Endpoints

### Create Ticket

POST `/tickets`

### Get All Tickets

GET `/tickets`

### Get Ticket By ID

GET `/tickets/{ticket_id}`

### Update Ticket

PUT `/tickets/{ticket_id}`

### Assign Ticket

PATCH `/tickets/{ticket_id}/assign`

### Close Ticket

PATCH `/tickets/{ticket_id}/close`

## Dashboard

Displays:

* Total tickets
* Open tickets
* Closed tickets
* Tickets by priority
* Tickets by category
* Tickets by assigned agent

## Run API

```bash
python -m uvicorn app.api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run Dashboard

```bash
streamlit run app/dashboard.py
```

## Future Improvements

* PostgreSQL database
* User authentication
* AWS deployment
* Email notifications
* Docker Compose deployment
* CI/CD pipeline using GitHub Actions
