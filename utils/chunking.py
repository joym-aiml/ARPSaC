from transformers import T5Tokenizer

# Load tokenizer once (can be reused by agents if needed)
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

def chunk_text(text: str, max_tokens: int = 400, overlap: int = 100) -> list[str]:
    """
    Splits the input text into overlapping chunks based on token count.

    Args:
        text (str): Full input text to split.
        max_tokens (int): Maximum tokens per chunk.
        overlap (int): Number of overlapping tokens between chunks.

    Returns:
        list of str: Chunks of text suitable for model input.
    """
    # Tokenize and get raw token IDs
    token_ids = tokenizer.encode(text, truncation=False)
    
    chunks = []
    start = 0
    while start < len(token_ids):
        end = min(start + max_tokens, len(token_ids))
        chunk_ids = token_ids[start:end]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)

        # Slide the window forward
        start += max_tokens - overlap

    return chunks
