from datetime import datetime
from schemas import ClientCreateInput
from sqlalchemy.ext.asyncio.session import async_session
from database.models import Bikes, Clients
from database.__init__ import async_session
from sqlalchemy.future import select


async def create_client(client: ClientCreateInput):
    async with async_session() as session:
        new_client = Clients(
            name=client.name,
            email=client.email,
            password=client.password,
            phone=client.phone,
            document=client.document,
            address=client.address,
            city=client.city,
            state=client.state,
            zip_code=client.zip_code,
            birthday=client.birthday,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)
        return new_client


async def get_client_by_email(email: str):
    async with async_session() as session:
        query = await session.execute(select(Clients).where(Clients.email == email))
        return query.scalars().first()


async def get_client_by_id(id: int):
    async with async_session() as session:
        query = await session.execute(select(Clients).where(Clients.id == id))
        return query.scalars().first()


async def create_bike(bike, client_id: int):
    async with async_session() as session:
        new_bike = Bikes(
            brand=bike['brand'],
            model=bike['model'],
            price=float(bike['price']),
            year=int(bike['year']),
            color=bike['color'],
            serial_number=bike['serial_number'],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            client_id=client_id
        )
        session.add(new_bike)
        await session.commit()
        await session.refresh(new_bike)
        return new_bike


async def get_all_bikes(client_id: int):
    async with async_session() as session:
        query = await session.execute(select(Bikes).where(Bikes.client_id == client_id))
        return query.scalars().all()


async def get_all_clients():
    async with async_session() as session:
        query = await session.execute(select(Clients))
        return query.scalars().all()
