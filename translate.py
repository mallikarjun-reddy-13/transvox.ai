from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {"en", "hi", "ta", "kn", "mr", "bn", "te"}


def translate_text(text, source_lang="en", target_lang="te"):
    """Translate text in chunks while respecting the provider's input limit."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("There is no text to translate.")
    if source_lang not in SUPPORTED_LANGUAGES or target_lang not in SUPPORTED_LANGUAGES:
        raise ValueError("Unsupported source or target language.")
    if source_lang == target_lang:
        raise ValueError("Source and target languages must be different.")

    max_chunk_size = 4500
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Avoid producing an empty chunk and handle unusually long tokens.
        while len(word) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            chunks.append(word[:max_chunk_size])
            word = word[max_chunk_size:]

        candidate = f"{current_chunk} {word}".strip()
        if len(candidate) > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = word
        else:
            current_chunk = candidate

    if current_chunk:
        chunks.append(current_chunk)

    translator = GoogleTranslator(source=source_lang, target=target_lang)
    translated_chunks = []
    for index, chunk in enumerate(chunks, start=1):
        print(f"Translating chunk {index}/{len(chunks)}...")
        translated = translator.translate(chunk)
        if not translated:
            raise RuntimeError(f"Translation failed for text chunk {index}.")
        translated_chunks.append(translated)

    return " ".join(translated_chunks).strip()
