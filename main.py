from fastapi import FastAPI

from api.routers.gun_router import router as gun_router

app = FastAPI(
    title="Shoot niggers 4 fun"
)

app.include_router(gun_router)
