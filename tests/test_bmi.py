from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_calculate_bmi_endpoint(client):
    response = client.post(
        "/api/bmi",
        json={"weight_kg": 70, "height_m": 1.75},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["bmi"] == pytest.approx(22.86, abs=0.01)
    assert data["category"] == "Normal weight"


def test_calculate_bmi_endpoint_rejects_invalid_input(client):
    response = client.post(
        "/api/bmi",
        json={"weight_kg": -1, "height_m": 1.75},
    )

    assert response.status_code == 400
