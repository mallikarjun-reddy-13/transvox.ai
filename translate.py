from deep_translator import GoogleTranslator

def translate_text(text, source_lang='en', target_lang='te'):
    """Translate text from source language to target language"""
    
    print(f"Translating from {source_lang} to {target_lang}...")
    
    # Split text into chunks (Google Translate has character limit)
    max_chunk_size = 4500
    chunks = []
    
    # Split long text into smaller chunks
    if len(text) > max_chunk_size:
        words = text.split(' ')
        current_chunk = ''
        
        for word in words:
            if len(current_chunk) + len(word) < max_chunk_size:
                current_chunk += word + ' '
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + ' '
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    else:
        chunks = [text]
    
    # Translate each chunk
    translated_chunks = []
    
    for i, chunk in enumerate(chunks):
        print(f"Translating chunk {i+1}/{len(chunks)}...")
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(chunk)
        translated_chunks.append(translated)
    
    # Join all translated chunks
    final_translation = ' '.join(translated_chunks)
    
    print(f"Translation complete!")
    print(f"Original: {text[:100]}...")
    print(f"Translated: {final_translation[:100]}...")
    
    return final_translation