
# llm_client.py

from abc import ABC, abstractmethod
from google import genai
import requests
import os
import time

from cost_calculator import calculate_cost


# 1. Common LLM Provider Interface
class LLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt):
        pass


# 2. Gemini Provider
class GeminiProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text


# 3. Ollama Provider
class OllamaProvider(LLMProvider):

    def __init__(self):
        self.model = "llama3.2"
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "")


# 4. LLM Client
class LLMClient:

    def __init__(self, provider):
        self.provider = provider

    def ask(self, prompt):

        for attempt in range(3):
            try:
                start_time = time.time()

                answer = self.provider.generate(prompt)

                elapsed_time = time.time() - start_time

                print(f"\nResponse generated in {elapsed_time:.2f} seconds")

                return answer

            except Exception as error:

                print(f"Attempt {attempt + 1} failed: {error}")

                if attempt < 2:
                    time.sleep(attempt + 1)

        raise RuntimeError("All AI provider attempts failed.")
