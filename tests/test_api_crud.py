"""CRUD endpoint tests for the EMS API."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db_session
from app.main import app
from app.models import Base


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Create a TestClient backed by an isolated in-memory database."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_db_session() -> Generator[Session, None, None]:
        db_session = testing_session_local()
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db_session] = override_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_all_resource_crud_flows(client: TestClient) -> None:
    """Create, read, update, and delete one record for every schema table."""
    user = _create(client, "/users/", {"full_name": "Ada Lovelace", "email": "ada@example.com", "password": "password123"})
    user_id = user["user_id"]
    _patch(client, f"/users/{user_id}", {"full_name": "Ada L."}, "full_name", "Ada L.")
    _get(client, f"/users/{user_id}", "user_id", user_id)

    site = _create(
        client,
        "/sites/",
        {"user_id": user_id, "site_name": "Main Campus", "latitude": 9.03, "longitude": 38.74},
    )
    site_id = site["site_id"]
    _patch(client, f"/sites/{site_id}", {"site_name": "Updated Campus"}, "site_name", "Updated Campus")

    device = _create(
        client,
        "/devices/",
        {
            "site_id": site_id,
            "device_name": "Main Smart Meter",
            "device_type": "SMART_METER",
            "manufacturer": "Siemens",
            "installed_at": "2026-01-01",
        },
    )
    device_id = device["device_id"]
    _patch(client, f"/devices/{device_id}", {"manufacturer": "ABB"}, "manufacturer", "ABB")

    energy_reading = _create(
        client,
        "/energy-readings/",
        {
            "device_id": device_id,
            "reading_time": "2026-06-23T00:00:00+00:00",
            "power_kw": "0.80",
            "energy_kwh": "0.80",
        },
    )
    _patch(client, f"/energy-readings/{energy_reading['reading_id']}", {"power_kw": "1.25"}, "power_kw", "1.25")

    solar_generation = _create(
        client,
        "/solar-generation/",
        {
            "device_id": device_id,
            "generated_at": "2026-06-23T10:00:00+00:00",
            "generated_kwh": "3.50",
        },
    )
    _patch(
        client,
        f"/solar-generation/{solar_generation['generation_id']}",
        {"generated_kwh": "4.00"},
        "generated_kwh",
        "4.00",
    )

    battery_status = _create(
        client,
        "/battery-status/",
        {
            "device_id": device_id,
            "recorded_at": "2026-06-23T12:00:00+00:00",
            "charge_percent": "75.00",
            "charge_kwh": "7.50",
        },
    )
    _patch(
        client,
        f"/battery-status/{battery_status['battery_status_id']}",
        {"charge_percent": "80.00"},
        "charge_percent",
        "80.00",
    )

    forecast = _create(
        client,
        "/forecasts/",
        {
            "site_id": site_id,
            "forecast_time": "2026-06-24T00:00:00+00:00",
            "predicted_kwh": "42.50",
            "model_name": "baseline",
        },
    )
    _patch(client, f"/forecasts/{forecast['forecast_id']}", {"model_name": "xgboost"}, "model_name", "xgboost")

    alert = _create(
        client,
        "/alerts/",
        {
            "site_id": site_id,
            "alert_type": "HIGH_CONSUMPTION",
            "message": "Consumption exceeded expected threshold.",
        },
    )
    _patch(client, f"/alerts/{alert['alert_id']}", {"status": "read"}, "status", "read")

    _delete(client, f"/alerts/{alert['alert_id']}")
    _delete(client, f"/forecasts/{forecast['forecast_id']}")
    _delete(client, f"/battery-status/{battery_status['battery_status_id']}")
    _delete(client, f"/solar-generation/{solar_generation['generation_id']}")
    _delete(client, f"/energy-readings/{energy_reading['reading_id']}")
    _delete(client, f"/devices/{device_id}")
    _delete(client, f"/sites/{site_id}")
    _delete(client, f"/users/{user_id}")


def _create(client: TestClient, path: str, payload: dict[str, object]) -> dict[str, object]:
    """POST a payload and return the created JSON record."""
    response = client.post(path, json=payload)
    assert response.status_code == 201, response.text
    return dict(response.json())


def _get(client: TestClient, path: str, id_field: str, expected_id: int) -> None:
    """GET one record and assert its identifier."""
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json()[id_field] == expected_id


def _patch(
    client: TestClient,
    path: str,
    payload: dict[str, object],
    field_name: str,
    expected_value: object,
) -> None:
    """PATCH one record and assert the changed field."""
    response = client.patch(path, json=payload)
    assert response.status_code == 200, response.text
    assert response.json()[field_name] == expected_value


def _delete(client: TestClient, path: str) -> None:
    """DELETE one record and assert it is gone."""
    response = client.delete(path)
    assert response.status_code == 204, response.text

    missing_response = client.get(path)
    assert missing_response.status_code == 404, missing_response.text
