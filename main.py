from typing import List, Optional

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from api.repositories.gun_repository import GunRepository
from api.routers.ammo_router import router as ammo_router
from api.routers.gun_router import router as gun_router, get_gun, get_guns_by_category
from api.routers.category_router import router as category_router, get_category
from api.routers.auth_router import router as auth_router
from starlette.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from starlette.staticfiles import StaticFiles

from api.routers.category_router import get_categories
from api.routers.gun_router import get_guns
from models.schemas import GunRead, CategoryRead
from utils.database import get_async_session

from fastapi import Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request


app = FastAPI(
    title="Test title",
    docs_url="/docs",
    redoc_url=None
)


app.include_router(gun_router)
app.include_router(category_router)
app.include_router(ammo_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return RedirectResponse(url='/mainPage')


app.mount("/static_main_page", StaticFiles(directory="frontend/main_page"), name="mainPage")
app.mount("/static_weapon_page", StaticFiles(directory="frontend/weaponpage"), name="weaponpage")
app.mount("/static_weapon_by_category", StaticFiles(directory="frontend/weapon_page_by_category"),
          name="weaponByCategoryPage")
app.mount("/static_weapon_by_name", StaticFiles(directory="frontend/weapon_page_by_name"), name="weaponPageByName")
app.mount("/static_admin_form_page", StaticFiles(directory="frontend/admin_register_form_page"),
          name="admin_register_form")


@app.get("/mainPage")
async def get_home_page(request: Request, categories: List[CategoryRead] = Depends(get_categories),
                        guns: List[GunRead] = Depends(get_guns)):
    main_page_template = Environment(loader=FileSystemLoader('.')).get_template('frontend/main_page/mainPage.html')

    context = {
        'categories': categories,
        'guns': guns,
    }

    data = main_page_template.render(context)
    return HTMLResponse(content=data)


@app.get("/api_tool")
async def get_api_tool_page(request: Request):
    main_page_template = Environment(loader=FileSystemLoader('.')).get_template(
        'frontend/admin_register_form_page/admin_register_form.html')
    data = main_page_template.render()
    return HTMLResponse(content=data)


@app.get("/gun/{category_id}/{gun_id}")
async def get_gun_page(request: Request, categories: List[CategoryRead] = Depends(get_categories),
                       category: CategoryRead = Depends(get_category), gun: GunRead = Depends(get_gun)):
    gun_page_template = Environment(loader=FileSystemLoader('.')).get_template('frontend/weaponpage/weaponpage.html')

    context = {
        'categories': categories,
        'category': category,
        'gun': gun,
    }

    data = gun_page_template.render(context)
    return HTMLResponse(content=data)


@app.get("/gun/{category_id}")
async def get_weapons_by_category_page(request: Request, category: CategoryRead = Depends(get_category),
                                       categories: List[CategoryRead] = Depends(get_categories),
                                       guns: List[GunRead] = Depends(get_guns_by_category)):
    weapon_by_category_template = Environment(loader=FileSystemLoader('.')).get_template(
        'frontend/weapon_page_by_category/weaponByCategoryPage.html')

    context = {
        'categories': categories,
        'category': category,
        'guns': guns,
    }

    data = weapon_by_category_template.render(context)
    return HTMLResponse(content=data)


@app.get("/gun/search/")
async def get_weapons_by_name_page(
        request: Request,
        query: Optional[str] = None,
        categories: List[CategoryRead] = Depends(get_categories),
        session: AsyncSession = Depends(get_async_session)
):
    weapon_by_name_template = Environment(loader=FileSystemLoader('.')).get_template(
        'frontend/weapon_page_by_name/weaponPageByName.html')

    gun_repository = GunRepository(session)
    print("gun_name:", query)

    if query:
        guns = await gun_repository.get_guns_by_name(query)
    else:
        guns = []

    context = {
        'categories': categories,
        'guns': guns,
    }

    data = weapon_by_name_template.render(context)
    return HTMLResponse(content=data)


add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
