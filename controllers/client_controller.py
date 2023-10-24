from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from auth import create_access_token, hash_password
from database.crud import create_client, get_all_clients
from controllers.auth_controller import verify_token

from schemas import (
    ClientCreateInput,
    TokenData
)

client_router = APIRouter(prefix='/client')


@client_router.post('/', description='Create a new client')
async def client_create(client_input: ClientCreateInput):
    try:
        client_input.password = hash_password(client_input.password)
        client = await create_client(client_input)
        token = create_access_token(
            data=TokenData(id=client.id, name=client.name))

        response = JSONResponse(
            content={'message': 'Sua conta foi criada com sucesso!'}, status_code=201)
        response.set_cookie("session", token, httponly=False,
                            secure=True, samesite="none")
        return response
    except Exception:
        raise HTTPException(
            500, detail={"message": "Houve um erro ao criar seu usuário"})


@client_router.get('/', description='Get client data')
async def client_get(request: Request):
    try:
        token = request.cookies.get("session")
        if not token:
            response = JSONResponse(
                content={'message': 'Sessão expirada, logue novamente!'}, status_code=401)
            response.set_cookie('session', expires=0,
                                max_age=0, secure=True, samesite='none')
            return response

        return await get_all_clients()
    except Exception as e:
        raise JSONResponse(500, content=str(e))
