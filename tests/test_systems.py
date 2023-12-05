import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import DDL

import src.entities as entities
from src.database import SCHEMA_NAME, engine
from src.main import app
from src.models import CreateSystem, System
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
        requests_mocker.post(
            "https://jsonplaceholder.typicode.com/users?email=test@gmail.com",  # Match the target URL.
            status_code=200,  # The status code of the response.
            json={"name": "tested"},  # Optional. The value when .json() is called on the response.
        )

        yield


async def test_planet_creation():
    request = CreateSystem(name="test", supreme_commander='test@gmail.com')

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/systems",
            content=request.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
    assert response.status_code == 200, response.text

    system = System.model_validate_json(response.content)
    assert system.name == request.name
    assert system.supreme_commander == request.supreme_commander
    assert system.id is not None
