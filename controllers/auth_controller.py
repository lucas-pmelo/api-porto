from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from auth import create_access_token, validate_token, verify_password
from database.crud import get_client_by_email
from schemas import LoginInput, TokenData


auth_router = APIRouter(prefix='/auth')


def session_exp(message, status_code=401):
    response = JSONResponse(
        content={'message': message}, status_code=status_code)
    response.set_cookie('session', expires=0, max_age=0,
                        secure=True, samesite='none')
    return response


@auth_router.post('/login', description='Login route')
async def login(login_input: LoginInput):
    client = await get_client_by_email(login_input.email)

    if not client:
        return session_exp('Email ou senha invalida', 404)

    if not verify_password(login_input.password, client.password):
        return session_exp('Email ou senha invalida')

    token = create_access_token(data=TokenData(id=client.id, name=client.name))
    response = JSONResponse(
        content={'message': 'Logado com sucesso!'}, status_code=200)
    response.set_cookie("session", token, httponly=False,
                        secure=True, samesite="none")
    return response


@auth_router.post('/logout', description='Logout route')
async def logout():
    return session_exp('Deslogado com sucesso!', 200)


@auth_router.get('/', description='Verify token and return client data')
async def verify_token(request: Request):
    token = request.cookies.get("session")
    if not token:
        return session_exp('Sessão expirada, logue novamente!')

    token_data = validate_token(token)
    if not token_data:
        return session_exp('Sessão expirada, logue novamente!')

    return JSONResponse(content={"name": token_data.name}, status_code=200)
