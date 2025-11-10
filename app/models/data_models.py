from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class WordInfo(BaseModel):
    word: str
    definition: str
    synonyms: List[str]
    examples: List[str]
    difficulty: DifficultyLevel

class TranslationRequest(BaseModel):
    text: str
    target_language: str

class Flashcard(BaseModel):
    word: str
    definition: str
    example: str
    difficulty: DifficultyLevel