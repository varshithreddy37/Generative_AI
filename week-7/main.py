import torch
import csv
from transformers import AutoTokenizer, AutoModelForCausalLM

# 1. Load a small open-source language model
MODEL_NAME = "openai-community/gpt2"

print("Loading GPT-2 model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()

print("Model loaded successfully!")

# 2. Define prompts
prompts = [
    "The cat is",
    "Artificial intelligence is",
    "India is a",
    "Machine learning helps"
]

TOP_K = 5
results = []

# 3. Inspect logits and probabilities
for prompt in prompts:
    print("\n" + "=" * 60)
    print("PROMPT:", prompt)
    print("=" * 60)

    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    print("Input Token IDs:", inputs["input_ids"][0].tolist())

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Logits for the next token position
    logits = outputs.logits[0, -1, :]

    # Convert logits into probabilities
    probabilities = torch.softmax(logits, dim=-1)

    # Get top-k candidates
    top_probs, top_ids = torch.topk(probabilities, TOP_K)

    print("\nTop", TOP_K, "Next-Token Candidates:")

    for prob, token_id in zip(top_probs, top_ids):
        token = tokenizer.decode([token_id.item()])
        print(f"Token: {token!r}, Probability: {prob.item():.4f}")