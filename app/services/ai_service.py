import json
import random
from typing import List, Dict
from googletrans import Translator, LANGUAGES
from deep_translator import GoogleTranslator
from app.models.data_models import DifficultyLevel, WordInfo, Flashcard
from app.utils.storage import JSONStorage
from app.services.external_api import ExternalAPIService


class LanguageAssistant:
    def __init__(self):
        self.storage = JSONStorage('data/vocabulary.json')
        self.external_api = ExternalAPIService()
        self.translator = Translator()
        self.initialize_vocabulary()

    def initialize_vocabulary(self):
        """Инициализира базовия речник ако не съществува"""
        default_vocab = {
            "words": {
                "здравей": {
                    "definition": "Поздравител при среща",
                    "synonyms": ["добър ден", "привет"],
                    "examples": ["Здравей, как си?"],
                    "difficulty": "beginner"
                },
                "благодаря": {
                    "definition": "Израз на благодарност",
                    "synonyms": ["мерси", "благодарствую"],
                    "examples": ["Благодаря за помощта!"],
                    "difficulty": "beginner"
                },
                "програма": {
                    "definition": "Последователност от инструкции",
                    "synonyms": ["софтуер", "приложение"],
                    "examples": ["Тази програма е много полезна."],
                    "difficulty": "intermediate"
                },
                "алгоритъм": {
                    "definition": "Стъпково решение на проблем",
                    "synonyms": ["метод", "процедура"],
                    "examples": ["Този алгоритъм е много ефективен."],
                    "difficulty": "advanced"
                },
                "компютър": {
                    "definition": "Електронно устройство за обработка на данни",
                    "synonyms": ["сметач", "ПК"],
                    "examples": ["Компютърът е включен цял ден."],
                    "difficulty": "beginner"
                },
                "програмист": {
                    "definition": "Човек, който пише компютърни програми",
                    "synonyms": ["разработчик", "кодер"],
                    "examples": ["Той е добър програмист."],
                    "difficulty": "intermediate"
                }
            }
        }
        if not self.storage.file_exists():
            self.storage.save_data(default_vocab)

    def translate_text(self, text: str, target_lang: str = "en") -> str:
        """Превежда текст с Google Translate"""
        try:
            # Първи метод: googletrans
            translated = self.translator.translate(text, dest=target_lang)
            return translated.text
        except Exception as e:
            print(f"Googletrans error: {e}")
            try:
                # Втори метод: deep-translator
                language_map = {
                    'en': 'english',
                    'es': 'spanish',
                    'fr': 'french',
                    'de': 'german',
                    'it': 'italian',
                    'ru': 'russian'
                }
                target_lang_name = language_map.get(target_lang, 'english')
                translated = GoogleTranslator(source='auto', target=target_lang_name).translate(text)
                return translated
            except Exception as e2:
                print(f"Deep-translator error: {e2}")
                # Fallback към симулиран превод
                return self._get_mock_translation(text, target_lang)

    def _get_mock_translation(self, text: str, target_lang: str) -> str:
        """Симулира превод ако API не работи"""
        mock_translations = {
            "en": {
                "здравей": "hello",
                "благодаря": "thank you",
                "програма": "program",
                "компютър": "computer",
                "език": "language",
                "учене": "learning",
                "приложение": "application",
                "интелигентен": "intelligent"
            },
            "es": {
                "здравей": "hola",
                "благодаря": "gracias",
                "програма": "programa",
                "компютър": "computadora",
                "език": "idioma",
                "учене": "aprendizaje",
                "приложение": "aplicación",
                "интелигентен": "inteligente"
            },
            "fr": {
                "здравей": "bonjour",
                "благодаря": "merci",
                "програма": "programme",
                "компютър": "ordinateur",
                "език": "langue",
                "учене": "apprentissage",
                "приложение": "application",
                "интелигентен": "intelligent"
            },
            "de": {
                "здравей": "hallo",
                "благодаря": "danke",
                "програма": "programm",
                "компютър": "computer",
                "език": "sprache",
                "учене": "lernen",
                "приложение": "anwendung",
                "интелигентен": "intelligent"
            }
        }

        # Проверка за директно съвпадение
        if text.lower() in mock_translations.get(target_lang, {}):
            return mock_translations[target_lang][text.lower()]

        # Генериране на превод на базата на езика
        lang_names = {
            "en": "английски",
            "es": "испански",
            "fr": "френски",
            "de": "немски"
        }
        lang_name = lang_names.get(target_lang, "английски")
        return f"Превод на '{text}' на {lang_name} език"

    def get_synonyms(self, word: str) -> List[str]:
        """Връща списък с синоними на думата"""
        vocabulary = self.storage.load_data()
        word_data = vocabulary["words"].get(word.lower())
        if word_data:
            return word_data.get("synonyms", [])

        # Генериране на симулирани синоними
        mock_synonyms = {
            "добър": ["хубав", "качествен", "отличен", "превъзходен"],
            "голям": ["обемен", "просторен", "огромен", "мащабен"],
            "малък": ["дребен", "миниатюрен", "съвсем малък", "неголям"],
            "бърз": ["пъргав", "ефективен", "светкавичен", "стремителен"],
            "красив": ["прекрасен", "великолепен", "очарователен", "изящен"],
            "умен": ["интелигентен", "съобразителен", "разумен", "мъдър"]
        }
        return mock_synonyms.get(word.lower(), [f"синоним_1_{word}", f"синоним_2_{word}"])

    def get_word_info(self, word: str) -> Dict:
        """Връща информация за думата"""
        vocabulary = self.storage.load_data()
        word_data = vocabulary["words"].get(word.lower())

        if word_data:
            return word_data

        # Симулирана AI логика за генериране на информация за нова дума
        return {
            "definition": f"Дефиниция за {word}",
            "synonyms": self.get_synonyms(word),
            "examples": [f"Примерно изречение с думата {word}."],
            "difficulty": self.assess_difficulty(word)
        }

    def assess_difficulty(self, word: str) -> str:
        """Оценява трудността на думата (симулирана AI логика)"""
        word_length = len(word)
        complex_letters = {'ж', 'ч', 'ш', 'щ', 'ю', 'я'}
        complex_count = sum(1 for letter in word.lower() if letter in complex_letters)

        if word_length <= 5 and complex_count == 0:
            return DifficultyLevel.BEGINNER
        elif word_length <= 8 and complex_count <= 1:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.ADVANCED

    def get_word_of_day(self) -> Dict:
        """Връща думата на деня"""
        vocabulary = self.storage.load_data()
        words = list(vocabulary["words"].keys())
        selected_word = random.choice(words)
        word_data = vocabulary["words"][selected_word]

        return {
            "word": selected_word,
            "definition": word_data["definition"],
            "synonyms": word_data["synonyms"],
            "examples": word_data["examples"],
            "difficulty": word_data["difficulty"]
        }

    def generate_flashcards(self, count: int = 10) -> List[Flashcard]:
        """Генерира флаш карти за учене"""
        vocabulary = self.storage.load_data()
        words = list(vocabulary["words"].items())

        flashcards = []
        for word, data in words[:count]:
            flashcards.append(Flashcard(
                word=word,
                definition=data["definition"],
                example=data["examples"][0] if data["examples"] else f"Пример с {word}",
                difficulty=data["difficulty"]
            ))

        return flashcards

    def get_supported_languages(self) -> Dict[str, str]:
        """Връща поддържаните езици за превод"""
        return {
            "en": "Английски",
            "es": "Испански",
            "fr": "Френски",
            "de": "Немски",
            "it": "Италиански",
            "ru": "Руски"
        }