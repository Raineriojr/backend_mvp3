from pydantic import BaseModel


class UserSchema(BaseModel):
    """Schema para criação de usuário"""

    name: str = "Rainério"
    email: str = "email@email.com"
    password: str = "senha@123"


class UserViewSchema(BaseModel):
    """Schema para retorno de usuário criado"""

    id: int = "1"


def create_user_response(user: UserViewSchema):
    return {
        "id": user.id
    }
