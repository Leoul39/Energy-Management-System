# Energy Management System

A portfolio-quality Energy Management System (EMS) for storing, analyzing, forecasting, and visualizing building energy usage.

## Current Scope

This repository currently contains the PostgreSQL schema and seed data, plus the initial FastAPI backend structure with SQLAlchemy models that match `database/schema.sql` and Pydantic schemas for request and response validation.

## Backend Layers

- `backend/app/models/`: SQLAlchemy ORM mappings for the existing PostgreSQL tables.
- `backend/app/schemas/`: Pydantic v2 schemas that define API input and output shapes.
- `backend/app/crud/`: reusable database operations for creating, reading, updating, and deleting records.
- `backend/app/routers/`: FastAPI route modules for each EMS resource.
- `backend/app/database.py`: SQLAlchemy engine and session management.
- `backend/app/main.py`: FastAPI application entrypoint.

## API Endpoints

The backend currently exposes CRUD endpoints for:

- `/users`
- `/sites`
- `/devices`
- `/energy-readings`
- `/solar-generation`
- `/battery-status`
- `/forecasts`
- `/alerts`

Each resource supports:

- `GET /resource/`
- `GET /resource/{record_id}`
- `POST /resource/`
- `PATCH /resource/{record_id}`
- `DELETE /resource/{record_id}`

## Testing

Run the automated CRUD endpoint tests from the project root:

```bash
python -m pytest -q
```

Run the API locally for Postman testing:

```bash
cd backend
uvicorn app.main:app --reload
```

Then open the generated API docs:

```text
http://127.0.0.1:8000/docs
```
