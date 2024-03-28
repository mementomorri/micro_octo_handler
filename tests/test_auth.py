from datetime import date

from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "mementomorimore@gmail.com",
            "password": "verySecretPassword",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "paid_access": False,
            "free_messages_left": 10,
            "refresh_at": str(date.today()),
        },
    )

    assert response.status_code == 201


async def test_login(ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "grant_type": None,
            "username": "mementomorimore@gmail.com",
            "password": "verySecretPassword",
            "scope": None,
            "client_id": None,
            "client_secret": None,
        },
    )

    assert response.status_code == 200
