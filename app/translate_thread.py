"""
Translation thread module
"""
import json

import requests
from PyQt6.QtCore import QThread, pyqtSignal


class TranslateThread(QThread):
    """Thread for performing translation"""

    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    chunk_received = pyqtSignal(str)
    alternatives_ready = pyqtSignal(list)

    def __init__(self, api_key, model, prompt, get_alternatives=False):
        super().__init__()
        self.api_key = api_key
        self.model = model
        self.prompt = prompt
        self.get_alternatives = get_alternatives

    def run(self):
        try:
            # Main translation
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional translator. Translate accurately and naturally.",
                        },
                        {"role": "user", "content": self.prompt},
                    ],
                    "temperature": 0.3,
                    "stream": True,
                },
                timeout=30,
                stream=True,
            )

            if response.status_code == 200:
                full_translation = ""
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode("utf-8")
                        if line_text.startswith("data: "):
                            data_str = line_text[6:]
                            if data_str.strip() == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        full_translation += content
                                        self.chunk_received.emit(full_translation)
                            except json.JSONDecodeError:
                                pass

                self.finished.emit(full_translation)

                # Get alternative translations
                if self.get_alternatives and full_translation:
                    self.get_alternative_translations()
            else:
                error_msg = (
                    response.json()
                    .get("error", {})
                    .get("message", "Unknown error")
                )
                self.error.emit(f"API Error: {error_msg}")

        except Exception as e:
            self.error.emit(f"Error: {str(e)}")

    def get_alternative_translations(self):
        """Get alternative translation options"""
        try:
            alt_prompt = (
                self.prompt
                + "\n\nSuggest 3 alternative translation options in the format:\n1. [option 1]\n2. [option 2]\n3. [option 3]"
            )

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional translator. Suggest different stylistic translation variants.",
                        },
                        {"role": "user", "content": alt_prompt},
                    ],
                    "temperature": 0.7,
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                alternatives_text = result["choices"][0]["message"]["content"].strip()

                # Parse alternatives
                alternatives = []
                for line in alternatives_text.split("\n"):
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-")):
                        # Remove numbering
                        clean_line = (
                            line.split(".", 1)[-1].strip()
                            if "." in line
                            else line.lstrip("- ")
                        )
                        if clean_line:
                            alternatives.append(clean_line)

                if alternatives:
                    self.alternatives_ready.emit(alternatives[:3])

        except Exception as e:
            print(f"Error getting alternatives: {e}")
