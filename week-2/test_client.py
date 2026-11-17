import pytest
from llm_client import LLMClient


class FakeProvider:

    def generate(self, prompt):
        return "AI stands for Artificial Intelligence."


def test_generate():
    provider = FakeProvider()
    client = LLMClient(provider)

    result = client.generate("Explain AI")

    assert result == "AI stands for Artificial Intelligence."


if __name__ == "__main__":
    pytest.main()