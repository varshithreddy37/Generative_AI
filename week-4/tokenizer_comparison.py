
from transformers import AutoTokenizer

# Input text
text = "Artificial intelligence is changing the world."

# Load tokenizers
print("Loading GPT-2...")
gpt2 = AutoTokenizer.from_pretrained("gpt2")

print("Loading Multilingual BERT...")
bert = AutoTokenizer.from_pretrained(
    "bert-base-multilingual-cased"
)

print("Loading SentencePiece - XLM-R...")
xlmr = AutoTokenizer.from_pretrained(
    "xlm-roberta-base"
)

# Function to compare tokenizers
def compare_tokenizer(name, tokenizer, text):
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)

    print("\n", name)
    print("Tokens:", tokens)
    print("Token IDs:", token_ids)
    print("Token count:", len(tokens))


print("\n==============================")
print("LANGUAGE: English")
print("INPUT TEXT:", text)
print("==============================")

compare_tokenizer("GPT-2", gpt2, text)

compare_tokenizer("Multilingual BERT", bert, text)

compare_tokenizer("SentencePiece - XLM-R", xlmr, text)
