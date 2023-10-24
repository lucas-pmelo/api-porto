from fastapi import APIRouter, Request, File, Form
from fastapi.responses import JSONResponse
from auth import validate_token
from database.crud import create_bike, get_all_bikes
from ia.ia_bike import analyse_image

bike_router = APIRouter(prefix='/bike')


@bike_router.post('/', description='Create a new bike')
async def bike_create(
    request: Request,
    photo: bytes = File(),
    brand=Form(),
    model=Form(),
    price=Form(),
    year=Form(),
    color=Form(),
    serial_number=Form()
):
    try:
        token = request.cookies.get("session")
        if not token:
            response = JSONResponse(
                content={'message': 'Sessão expirada, logue novamente!'}, status_code=401)
            response.set_cookie('session', expires=0,
                                max_age=0, secure=True, samesite='none')
            return response

        if not analyse_image(photo):
            return JSONResponse(
                content={'message': 'Não encontramos uma bicicleta na sua foto!'}, status_code=400)

        token_data = validate_token(token)
        bike_data = {
            'brand': brand,
            'model': model,
            'price': price,
            'year': year,
            'color': color,
            'serial_number': serial_number
        }

        await create_bike(bike_data, token_data.id)
        return JSONResponse(content={'message': 'Bike criada com sucesso!'}, status_code=201)
    except Exception as e:
        raise JSONResponse(400, content=str(e))


@bike_router.get('/', description='Get all bikes')
async def get_bikes(request: Request):
    try:
        token = request.cookies.get("session")
        if not token:
            response = JSONResponse(
                content={'message': 'Sessão expirada, logue novamente!'}, status_code=401)
            response.set_cookie('session', expires=0,
                                max_age=0, secure=True, samesite='none')
            return response

        token_data = validate_token(token)
        return await get_all_bikes(token_data.id)
    except Exception as e:
        raise JSONResponse(500, content=str(e))
