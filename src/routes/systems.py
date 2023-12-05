import datetime
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .. import entities, models
from ..database import get_db
import requests

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/systems", tags=["Systems"])


@router.post("", response_model=models.System)
async def create_system(
    request: models.CreateSystem, db: AsyncSession = Depends(get_db)
):
    system = entities.System()
    system.id = uuid4()
    system.name = request.name
    system.supreme_commander = request.supreme_commander
    response = requests.get(url='https://jsonplaceholder.typicode.com/users',
                            params={'email': request.supreme_commander})
    system.supreme_commander_name = response.json()[0].get('name', '')
    system.date_created = datetime.datetime.now()
    db.add(system)
    await db.commit()
    return system


@router.get("system_population/{system_id}")
async def get_system_population(
    system_id, db: AsyncSession = Depends(get_db)
):
    stmt = (await db.scalar(select(func.sum(entities.Planet.population_millions)).where(entities.Planet.system_id == system_id))
    )
    system = await db.execute(stmt)
    return system.scalars().first()
