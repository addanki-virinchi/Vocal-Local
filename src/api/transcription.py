"""
API module for handling transcription and translation requests.
"""

import os
import io
import openai
from ..core.config import API_KEY, SUPPORTED_LANGUAGES

def initialize_api():
    """Initialize the OpenAI API with our key."""
    openai.api_key = API_KEY
    os.environ["OPENAI_API_KEY"] = API_KEY

def transcribe_audio(audio_data, model="gpt-4o-mini-transcribe", language="en"):
    """Transcribe audio using OpenAI API."""
    try:
        # Prepare audio file for API
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.wav"
        
        # Send to API with specified language
        response = openai.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language
        )
        
        # Return transcription
        return response.text
        
    except Exception as e:
        print(f"Error transcribing with {model}: {e}")
        return None

def translate_text(text, target_language="en"):
    """Translate text to target language using OpenAI API."""
    try:
        # Get language name for better prompting
        language_name = next((name for name, code in SUPPORTED_LANGUAGES.items() 
                            if code == target_language), target_language)
        
        print(f"Translating to {language_name}...")
        
        # Call OpenAI API for translation
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {language_name}."},
                {"role": "user", "content": text}
            ]
        )
        
        # Return translation
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error translating: {e}")
        return None 