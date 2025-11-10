from fastapi import APIRouter, HTTPException
from app.services.ai_service import LanguageAssistant
from app.services.external_api import ExternalAPIService

router = APIRouter(prefix="/api/v1")
assistant = LanguageAssistant()
external_api = ExternalAPIService()


@router.get("/translate/{text}")
async def translate_text(text: str, target_lang: str = "en"):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        result = assistant.translate_text(text, target_lang)
        return {
            "original": text,
            "translated": result,
            "target_lang": target_lang,
            "source_lang": "auto"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@router.get("/synonyms/{word}")
async def get_synonyms(word: str):
    if not word.strip():
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    synonyms = assistant.get_synonyms(word)
    return {"word": word, "synonyms": synonyms}


@router.get("/word-info/{word}")
async def get_word_info(word: str):
    if not word.strip():
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    info = assistant.get_word_info(word)
    return {"word": word, "info": info}


@router.get("/difficulty-level/{word}")
async def get_difficulty_level(word: str):
    if not word.strip():
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    level = assistant.assess_difficulty(word)
    return {"word": word, "difficulty_level": level}


@router.get("/supported-languages")
async def get_supported_languages():
    languages = assistant.get_supported_languages()
    return {"languages": languages}