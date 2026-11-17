
# main.py

import os
from dotenv import load_dotenv

from llm_client import (
    GeminiProvider,
    OllamaProvider,
    LLMClient
)

from mongo_logger import MongoLogger


# Load environment variables
load_dotenv(override=True)


def main():

    print("\n==============================")
    print("       WEEK 3: LLM MONITORING")
    print("==============================")

    print("\n1. Gemini")
    print("2. Ollama")

    choice = input("\nSelect provider (1/2): ").strip()

    if choice == "1":
        provider_name = "gemini"
        provider = GeminiProvider()

    elif choice == "2":
        provider_name = "ollama"
        provider = OllamaProvider()

    else:
        print("Invalid choice!")
        return

    client = LLMClient(provider)
    logger = MongoLogger()

    try:
        question = input("\nEnter your question: ")

        if not question.strip():
            print("Question cannot be empty.")
            return

        answer = client.ask(question)

        print("\n========== AI RESPONSE ==========")
        print(answer)

        log_data = {
            "provider": provider_name,
            "question": question,
            "response": answer,
            "status": "success"
        }

        logger.log_call(log_data)

    except Exception as error:
        print("Error:", error)

    finally:
        logger.close()


if __name__ == "__main__":
    main()
