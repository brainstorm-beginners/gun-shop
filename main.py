from fastapi import FastAPI
from fastapi_pagination import add_pagination

from api.routers.ammo_router import router as ammo_router
from api.routers.gun_router import router as gun_router
from api.routers.category_router import router as category_router

app = FastAPI(
    title="Shoot niggers 4 fun"
)

app.server = {
    "host": "localhost",
    "port": 8000,
}

add_pagination(app)
app.include_router(gun_router)
app.include_router(category_router)
app.include_router(ammo_router)
