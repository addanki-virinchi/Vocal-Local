"""
VocalLocal Web Service - Flask API for speech-to-text
"""

import os
import io
import tempfile
import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())

# OpenAI API configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    print("Warning: OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

# Configure upload settings
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    print("Transcription API called")
    
    # Check if file was provided
    if 'file' not in request.files:
        print("Error: No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Log file information
    print(f"File received: {file.filename}, Content type: {file.content_type}")
    
    if file.filename == '':
        print("Error: Empty filename")
        return jsonify({'error': 'No selected file'}), 400
    
    # Check file extension
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    print(f"File extension: {file_ext}")
    
    if not allowed_file(file.filename):
        print(f"Error: Invalid file type '{file_ext}'. Allowed: {ALLOWED_EXTENSIONS}")
        return jsonify({'error': f'Invalid file type: .{file_ext}. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")
        
        # Get file size
        file_size = os.path.getsize(filepath)
        print(f"File size: {file_size} bytes")
        
        if file_size == 0:
            print("Error: File is empty")
            os.remove(filepath)
            return jsonify({'error': 'Uploaded file is empty'}), 400
        
        # Get parameters from form
        language = request.form.get('language', 'en')
        model = request.form.get('model', 'gpt-4o-mini-transcribe')
        translate_to = request.form.get('translate_to', None)
        speaker_id = request.form.get('speaker_id', '1')  # Default to speaker 1 if not specified
        
        print(f"Speaker ID: {speaker_id}")
        print(f"Transcription language: {language}")
        print(f"Transcription model: {model}")
        print(f"Translation target language: {translate_to}")
        
        # Process with OpenAI
        try:
            print(f"Sending to OpenAI API: model={model}, language={language}")
            with open(filepath, 'rb') as audio_file:
                response = openai.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    language=language
                )
            
            # Get the transcribed text
            transcribed_text = response.text
            translated_text = None
            
            # If translation is requested and the target language is different from the source
            if translate_to and translate_to != language:
                try:
                    print(f"Translating from {language} to {translate_to}")
                    from src.api.transcription import translate_text
                    translated_text = translate_text(transcribed_text, translate_to)
                except Exception as e:
                    print(f"Translation error: {str(e)}")
                    # Continue even if translation fails
            
            # Remove temporary file
            os.remove(filepath)
            print("Temporary file removed")
            
            # Return results
            result = {
                'text': transcribed_text,
                'language': language,
                'speaker_id': speaker_id,
                'success': True
            }
            
            # Add translation if available
            if translated_text:
                result['translated_text'] = translated_text
                result['translated_to'] = translate_to
                
            print(f"Transcription successful, text length: {len(transcribed_text)}")
            if translated_text:
                print(f"Translation successful, text length: {len(translated_text)}")
                
            return jsonify(result)
            
        except Exception as e:
            # Log detailed error information
            print(f"OpenAI API error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'OpenAI API error: {str(e)}'}), 500
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    # Dictionary of supported languages with their codes
    supported_languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Dutch": "nl",
        "Japanese": "ja",
        "Chinese": "zh",
        "Korean": "ko",
        "Russian": "ru",
        "Arabic": "ar",
        "Hindi": "hi",
        "Telugu": "te",
        "Turkish": "tr",
        "Swedish": "sv",
        "Polish": "pl",
        "Norwegian": "no",
        "Finnish": "fi",
        "Danish": "da",
        "Ukrainian": "uk",
        "Czech": "cs",
        "Romanian": "ro",
        "Hungarian": "hu",
        "Greek": "el",
        "Hebrew": "he",
        "Thai": "th",
        "Vietnamese": "vi",
        "Indonesian": "id",
        "Malay": "ms",
        "Bulgarian": "bg"
    }
    return jsonify(supported_languages)

if __name__ == '__main__':
    # Using 'adhoc' SSL context for development
    # This creates a self-signed certificate that browsers will warn about
    # but will still provide a secure context for MediaDevices API
    try:
        # First attempt to run with SSL for microphone access
        app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
    except Exception as e:
        print(f"Error running with SSL: {e}")
        print("Falling back to non-SSL mode. Note: Microphone access may not work in this mode.")
        # Fall back to regular HTTP if SSL fails (microphone won't work in most browsers)
        app.run(debug=True, host='0.0.0.0')