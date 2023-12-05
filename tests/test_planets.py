import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import DDL

import src.entities as entities
from src.database import SCHEMA_NAME, engine
from src.main import app
from src.models import CreatePlanet, Planet, CreateSystem, System
import requests_mock


@pytest.fixture(scope="session", autouse=True)
async def session_cleanup():
    yield

    async with engine.begin() as conn:
        await conn.execute(
            DDL(
                'TRUNCATE "%(schema)s"."%(table)s" CASCADE',
                {"schema": SCHEMA_NAME, "table": entities.Planet.__tablename__},
            )
        )


@pytest.fixture
def mock_post():
    with requests_mock.Mocker() as requests_mocker:
        requests_mocker.get(
            "https://jsonplaceholder.typicode.com/users?email=hello@gmail.com",  # Match the target URL.
            status_code=200,  # The status code of the response.
            json=[
                {"name": "tested"}
            ],  # Optional. The value when .json() is called on the response.
        )

        yield


async def test_planet_creation():
    system = CreateSystem(name="tested", supreme_commander="hello@gmail.com")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/systems",
            content=system.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
    system = System.model_validate_json(response.content)
    request = CreatePlanet(
        name="test", project_id=uuid.uuid4(), population_millions=1, system_id=system.id
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/planets",
            content=request.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
    assert response.status_code == 200, response.text

    planet = Planet.model_validate_json(response.content)
    assert planet.name == request.name
    assert planet.project_id == request.project_id
    assert planet.population_millions == request.population_millions
    assert planet.id is not None
