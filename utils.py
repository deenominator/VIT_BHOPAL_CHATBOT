import re

def clean_text(text: str) -> str:
    """
    Cleans text but KEEPS paragraphs/newlines so the structure isn't lost.
    """
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Splits text by characters (not words) to prevent cutting mid-sentence.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        
        if end < text_len:
            cut_point = text.rfind('\n', start, end)
            if cut_point == -1:
                cut_point = text.rfind(' ', start, end)
            
            if cut_point != -1:
                end = cut_point
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move forward, minus the overlap
        start = end - overlap
        
    return chunks