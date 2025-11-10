from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models.forms import ContactForm
from app.services.ai_service import LanguageAssistant

router = APIRouter()
templates = Jinja2Templates(directory="templates")
assistant = LanguageAssistant()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Начало"})

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "За проекта"})

@router.get("/contact", response_class=HTMLResponse)
async def contact_get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Контакт", "errors": None})

@router.post("/contact")
async def contact_post(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    form = ContactForm(name=name, email=email, message=message)
    errors = form.validate()
    if errors:
        return templates.TemplateResponse("contact.html", {"request": request, "title": "Контакт", "errors": errors}, status_code=400)
    return RedirectResponse(url="/?sent=1", status_code=303)

@router.get("/translator", response_class=HTMLResponse)
async def translator(request: Request):
    return templates.TemplateResponse("translator.html", {"request": request, "title": "Преводач"})

@router.get("/word-of-day", response_class=HTMLResponse)
async def word_of_day(request: Request):
    word_data = assistant.get_word_of_day()
    return templates.TemplateResponse("word_of_day.html", {"request": request, "title": "Дума на деня", "word_data": word_data})

@router.get("/flashcards", response_class=HTMLResponse)
async def flashcards(request: Request):
    flashcards_data = assistant.generate_flashcards()
    return templates.TemplateResponse("flashcards.html", {"request": request, "title": "Флаш карти", "flashcards": flashcards_data})