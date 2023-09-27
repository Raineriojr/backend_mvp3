from flask import Flask, redirect, request, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
import requests
from datetime import datetime
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from models import Session, User, Friend
from schemas import *

from logger import logger

info = Info(
    title="MVP 3 - Projeto",
    description="API para MVP 3 de Eng. de Software",
    version="1.0.0",
)


app: Flask = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}})

# tags
doc_tag = Tag(name="Documentação",
              description="Documentação de rotas da aplicação")
login_tag = Tag(name="Login", description="Login da aplicação")
register_tag = Tag(name="Cadastro de usuário",
                   description="CRUD de cadastro de usuário")
user_list_tag = Tag(name="Lista de Usuários Fake",
                    description="Retorna lista de usuários fakes")

friend_list_tag = Tag(name="Lista de amigos",
                      description="Retorna lista de amigos cadastrados")
friend_create_tag = Tag(name="Cadastro de amigo",
                        description="Rota para cadastro de amigo")
friend_update_tag = Tag(name="Altera dados de amigo",
                        description="Rota para update de amigo")
friend_delete_tag = Tag(name="Remover um amigo",
                        description="Remove um amigo da sua lista de amizades")


@app.get("/", tags=[doc_tag])
def index():
    """Retorna documentação da API no swagger"""
    return redirect("openapi/swagger")


@app.post(
    '/register',
    tags=[register_tag],
    responses={"200": UserViewSchema, "404": ErrorSchema, "400": ErrorSchema}
)
def register(body: UserSchema):
    """Realiza cadastro na aplicação"""

    try:
        user_data = UserSchema.parse_obj(request.get_json())
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )

        session = Session()

        session.add(user)
        session.commit()

        return create_user_response(user), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao cadastrar novo usuário: {e}")
        return {"IntegrityError": f"Usuário já registrado"}, 409

    except Exception as e:
        logger.warning(f"Erro ao cadastrar novo usuário: {e}")
        return {"error": f"Erro ao cadastrar novo usuário: {e}"}, 400


@app.post(
    '/login',
    tags=[login_tag],
    responses={"200": UserLoginViewSchema,
               "404": ErrorSchema, "400": ErrorSchema}
)
def login(body: UserLoginSchema):
    """Realiza login na aplicação"""

    try:
        login_data = UserLoginSchema.parse_obj(request.get_json())

        session = Session()

        with session.begin():
            user = session.query(User).filter_by(
                email=login_data.email).first()

            if not user:
                logger.warning("Usuário não existe na base.")
                return {"message": "Usuário ou senha incorretos"}, 400

        session.commit()

        if user.email == login_data.email and user.password == login_data.password:
            return get_user_data(user), 200
        else:
            return {"message": "Usuário ou senha incorretos"}, 400

    except Exception as e:
        logger.warning(f"Erro ao fazer login: {e}")
        return {"error": f"Erro ao fazer login: {e}"}, 400
    finally:
        session.close()

# ----------------------------------------------------------- #
# api externa


@app.get("/users_list", tags=[user_list_tag])
def fakeUsers():
    """Retorna lista de usuários falsos"""

    try:
        url = "https://randomuser.me/api/?results=5"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return logger.warning(f'A solicitação falhou com o status: {response.status_code}')

    except Exception as e:
        return logger.warning(f'A solicitação falhou: {response.status_code} - {e}')

# ----------------------------------------------------------- #


@app.get("/friends_list", tags=[user_list_tag], responses={"200": FriendViewSchema, "404": ErrorSchema},)
def friends_list():
    """Retorna lista de amigos"""

    authorization_header = request.headers.get('Authorization')

    if not authorization_header:
        return {"error": "Erro ao listar contatos. Necessário autorização"}, 401

    try:
        session = Session()

        friends = (
            session.query(Friend)
            .where(authorization_header == Friend.user_id)
            .group_by(Friend.name)
            .order_by(Friend.name.asc())
            .all()
        )

        if not friends:
            return {"friends": []}, 200
        else:
            return list_friends(friends), 200

    except Exception as e:
        logger.warning(f"Erro ao listar amigos: {e}")
        return {"error": f"Erro ao listar amigos: {e}"}, 400

    finally:
        session.close()


@app.post(
    "/friends/create",
    tags=[friend_create_tag],
    responses={"200": FriendViewSchema, "404": ErrorSchema},
)
def createContact(body: FriendSchema):
    """Cadastra um novo contato"""
    try:
        friend_data = FriendSchema.parse_obj(request.get_json())

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return {"error": "Erro ao cadastrar novo amigo. Necessário autorização"}, 401

        session = Session()

        user_exists = (
            session.query(User)
            .where(authorization_header == User.id)
            .first()
        )

        friend = Friend(
            name=friend_data.name,
            email=friend_data.email,
            country=friend_data.country,
            user_id=user_exists.id
        )

        session.add(friend)

        session.commit()

        return {"message": 'Novo amigo cadastrado com sucesso'}, 200

    except IntegrityError as e:
        logger.warning(f"Erro ao cadastrar novo amigo: {e}")
        return {"IntegrityError": f"Erro ao cadastrar novo amigo: {e}"}, 409

    except Exception as e:
        logger.warning(f"Erro ao cadastrar novo amigo: {e}")
        return {"error": f"Erro ao cadastrar novo amigo: {e}"}, 400


@app.put(
    "/friends/<int:friend_id>/update",
    tags=[friend_update_tag],
    responses={"200": FriendResponseSchema, "400": ErrorSchema},
)
def contactUpdate(path: FriendRemoveUpdateSchema, body: FriendUpdateSchema):
    authorization_header = request.headers.get('Authorization')
    friend_id: int = request.view_args.get("friend_id")
    friend_data = FriendUpdateSchema.parse_obj(request.get_json())

    if not authorization_header:
        return {"error": "Erro ao cadastrar novo amigo. Necessário autorização"}, 401

    try:
        session = Session()

        with session.begin():
            friend: Friend = (
                session.query(Friend)
                .where(Friend.user_id == authorization_header)
                .filter(Friend.id == friend_id)
                .first()
            )

            if not friend:
                logger.warning("Amigo não existe na base.")
                return {"message": "Amigo não existe na base."}, 404

            friend.name = friend_data.name
            friend.email = friend_data.email
            friend.country = friend_data.country
            friend.updated_at = datetime.now()

        session.commit()
        return (
            jsonify(**{"updated_at": friend.updated_at},
                    **show_friend(friend)),
            200,
        )

    except Exception as e:
        session.rollback()
        logger.warning(f"Falha ao alterar dados de amigo. {e}")
        return {"error": f"Falha ao alterar dados de amigo. {e}"}, 400

    finally:
        session.close()


@app.delete(
    "/friends/<int:friend_id>/delete",
    tags=[friend_delete_tag],
    responses={"200": FriendResponseSchema, "400": ErrorSchema},
)
def deleteContact(path: FriendRemoveUpdateSchema):
    authorization_header = request.headers.get('Authorization')
    friend_id: int = request.view_args.get("friend_id")

    if not authorization_header:
        return {"error": "Erro ao remover amigo. Necessário autorização"}, 401

    try:
        session = Session()

        count = session.query(Friend).where(
            Friend.user_id == authorization_header).filter(Friend.id == friend_id).delete()

        session.commit()

        if count:
            return {"message": f"Amigo removido - id: {friend_id}"}, 200
        else:
            logger.warning("Amigo não existe na base")
            return {"message": "Amigo não existe na base"}, 404

    except Exception as e:
        logger.warning(f"Falha ao remover amigo. {e}")
        return {"error": f"Falha ao remover amigo. {e}"}, 400

    finally:
        session.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
