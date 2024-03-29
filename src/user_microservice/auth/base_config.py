from time import time

from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
import jwt

from auth.manager import get_user_manager
from auth.models import User

from conf import AUTH_SECRET, TOKEN_ALGORITHM, TOKEN_LIFETIME


cookie_transport = CookieTransport(cookie_name="octo_handler_user", cookie_max_age=3600)


class OctoJWTStrategy(JWTStrategy):
    """
    Наследуюсь от стандартной стратегии записи данных в токен,
    чтобы видоизменить хранимые данные
    """

    async def write_token(self, user: models.UP) -> str:
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "exp": int(time() + int(self.lifetime_seconds)),
            "email": str(user.email),
            "paid_access": bool(user.paid_access),
            "free_messages_left": int(user.free_messages_left),
            "refresh_at": str(user.refresh_at),
        }
        return jwt.encode(data, str(self.secret))


def get_jwt_strategy() -> OctoJWTStrategy:
    return OctoJWTStrategy(
        secret=AUTH_SECRET, lifetime_seconds=TOKEN_LIFETIME, algorithm=TOKEN_ALGORITHM
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
