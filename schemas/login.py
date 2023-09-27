from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    """Schema para login de usuário"""

    email: str = "email@email.com"
    password: str = "senha@123"


class UserLoginViewSchema(BaseModel):
    """Schema de retorno de login"""

    id: int = 1
    name: str = "Rainério"
    email: str = "email@email.com"
    token: str = "qwertyuiop"


def get_user_data(user: UserLoginViewSchema):
    """Retorna dados do usuário após login"""

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "token": '881ED50041A343B16D935497EEC6367823DCFBA9F546EBEEDAAF927B5941C07E'
    }
