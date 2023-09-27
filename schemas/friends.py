from pydantic import BaseModel
from typing import List
from models.friends import Friend

class FriendSchema(BaseModel):
    """Schema para cadastro de amigo"""

    name: str = "Maria"
    email: str = "maria@email.com"
    country: str = "Brasil"


class FriendViewSchema(BaseModel):
    """Schema para listagem de amigos"""

    friend_id: str = 1
    name: str = "Maria"
    email: str = "maria@email.com"
    country: str = "Brasil"


class FriendUpdateSchema(BaseModel):
    """Schema para update de amigo"""

    friend_id: int = 1
    name: str = "Nova Maria"
    email: str = "novamaria@email.com"
    country: str = "Brasil"


class FriendRemoveUpdateSchema(BaseModel):
    """Schema para remover e atualizar amigo"""

    id: str = 1


class FriendResponseSchema(BaseModel):
    """Schema para retorno de delete e update"""

    message: str = ""



class ListFriendsSchema(BaseModel):
    """Define os parâmetros para listagem de amigos"""

    friends: List[FriendViewSchema]


def list_friends(friends: List[Friend]):
    """Retorna a representação dos amigos como definido em ListViewSchema"""
    result = []
    for friend in friends:
        result.append(
            {
                "id": friend.id,
                "name": friend.name,
                "email": friend.email,
                "country": friend.country,
            }
        )
    return {"friends": result}


def show_friend(friend: Friend):
    """Retorna a representação de um amigo"""
    return {
        "id": friend.id,
        "name": friend.name,
        "email": friend.email,
        "country": friend.country,
    }