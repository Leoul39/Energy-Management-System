# Energy Management System

A portfolio-quality Energy Management System (EMS) for storing, analyzing, forecasting, and visualizing building energy usage.

## Current Scope

This repository currently contains the PostgreSQL schema and seed data, plus the initial FastAPI backend structure with SQLAlchemy models that match `database/schema.sql` and Pydantic schemas for request and response validation.

## Backend Layers

- `backend/app/models/`: SQLAlchemy ORM mappings for the existing PostgreSQL tables.
- `backend/app/schemas/`: Pydantic v2 schemas that define API input and output shapes.
- `backend/app/database.py`: SQLAlchemy engine and session management.
- `backend/app/main.py`: FastAPI application entrypoint.
