from datetime import datetime
from pydantic import BaseModel


class SucessAuthOutput(BaseModel):
    message: str


class ErrorOutput(BaseModel):
    message: str


class TokenData(BaseModel):
    id: int
    name: str


class ClientCreateInput(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    document: str
    address: str
    city: str
    state: str
    zip_code: str
    birthday: datetime


class BikeCreateInput(BaseModel):
    brand: str
    model: str
    price: float
    year: int
    color: str
    serial_number: str


class LoginInput(BaseModel):
    email: str
    password: str


class VerifyTokenOutput(BaseModel):
    name: str
