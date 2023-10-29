from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination, Page
from fastapi_pagination.utils import disable_installed_extensions_check
from sqlalchemy.ext.asyncio import AsyncSession

from api.routers.ammo_router import router as ammo_router
from api.routers.gun_router import router as gun_router, get_gun
from api.routers.category_router import router as category_router, get_category
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader
from starlette.staticfiles import StaticFiles

from api.routers.category_router import get_categories
from api.routers.gun_router import get_guns
from models.schemas import GunRead, CategoryRead
from utils.database import get_async_session

app = FastAPI(
    title="Test title"
)

app.include_router(gun_router)
app.include_router(category_router)
app.include_router(ammo_router)


@app.get("/")
def root():
    return RedirectResponse(url='/mainPage')


app.mount("/static_main_page", StaticFiles(directory="frontend/main_page"), name="mainPage")
app.mount("/static_weapon_page", StaticFiles(directory="frontend/weaponpage"), name="weaponpage")


@app.get("/mainPage")
async def get_home_page(request: Request, categories: List[CategoryRead] = Depends(get_categories), guns: List[GunRead] = Depends(get_guns)):
    main_page_template = Environment(loader=FileSystemLoader('.')).get_template('frontend/main_page/mainPage.html')

    print("\n\nCATEGORIES:", type(categories))
    print(categories, end="\n\n")
    print("\n\nGUNS:", type(guns))
    print(guns, end="\n\n")

    context = {
        'categories': categories,
        'guns': guns,
    }

    data = main_page_template.render(context)
    return HTMLResponse(content=data)


@app.get("/gun/{category_id}/{gun_id}")
async def get_gun_page(request: Request, categories: List[CategoryRead] = Depends(get_categories), category: CategoryRead = Depends(get_category), gun: GunRead = Depends(get_gun)):
    gun_page_template = Environment(loader=FileSystemLoader('.')).get_template('frontend/weaponpage/weaponpage.html')

    context = {
        'categories': categories,
        'category': category,
        'gun': gun,
    }

    data = gun_page_template.render(context)
    return HTMLResponse(content=data)

add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
