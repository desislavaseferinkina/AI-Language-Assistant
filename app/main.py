from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.web import router as web_router
from app.controllers.api import router as api_router

app = FastAPI(title='AI Language Assistant')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(web_router)
app.include_router(api_router)