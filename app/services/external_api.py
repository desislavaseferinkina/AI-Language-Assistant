import httpx
import asyncio
from typing import Dict, Optional


class ExternalAPIService:
    def __init__(self):
        self.base_url = "https://api.example.com"  # Симулиран URL

    async def mock_api_call(self, endpoint: str, data: Dict) -> Dict:
        """Симулира извикване на външен API"""
        # Симулира мрежово забавяне
        await asyncio.sleep(0.5)

        # Симулирани отговори за различни endpoints
        mock_responses = {
            "translate": {"translated_text": f"Translated: {data.get('text', '')}"},
            "dictionary": {"definition": f"Definition of {data.get('word', '')}"},
            "thesaurus": {"synonyms": [f"synonym_{i}" for i in range(3)]}
        }

        return mock_responses.get(endpoint, {"status": "success", "data": data})

    async def get_translation(self, text: str, target_lang: str) -> str:
        """Взима превод от външен API (симулирано)"""
        response = await self.mock_api_call("translate", {"text": text, "target_lang": target_lang})
        return response.get("translated_text", text)

    async def get_definition(self, word: str) -> str:
        """Взима дефиниция от външен API (симулирано)"""
        response = await self.mock_api_call("dictionary", {"word": word})
        return response.get("definition", f"Definition for {word}")