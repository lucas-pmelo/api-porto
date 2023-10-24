from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import auth_router
from controllers.client_controller import client_router
from controllers.bike_controller import bike_router

app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000",
#     "http://localhost",
#     "localhost",
#     "http://localhost:8080",
#     "https://o2future.netlify.app"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["POST", "GET", "PUT", "DELETE"],
#     allow_headers=["*"],
#     max_age=3600,
#     expose_headers=["set-cookie"]
# )

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(bike_router)
