from llm_client import LLMClient, OllamaProvider

# Create the provider
provider = OllamaProvider()

# Create common client
client = LLMClient(provider)

# Get user question
prompt = input("Enter your question: ")

# Generate response
answer = client.generate(prompt)

print("\nLLM Response:")
print(answer)