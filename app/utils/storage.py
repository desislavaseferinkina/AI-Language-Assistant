import json
import os
from typing import Dict, Any


class JSONStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def file_exists(self) -> bool:
        return os.path.exists(self.file_path)

    def load_data(self) -> Dict[str, Any]:
        if not self.file_exists():
            return {}

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self, data: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)