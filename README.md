# VocalLocal

A bilingual conversation tool for real-time transcription and translation.

## Features

- **Two-Person Bilingual Conversation Interface**
  - Each user speaks in their native language
  - Real-time transcription of speech
  - Automatic translation to the other user's language
  - Display of both original and translated text

- **Language Selection**
  - Manual selection of spoken language for each participant
  - Support for 30+ languages

- **Text-to-Speech Functionality**
  - Optional TTS for translated messages
  - Toggle on/off for each participant

- **Browser & Device Compatibility**
  - Support for modern browsers (Chrome, Firefox, Safari)
  - Mobile device support including iOS
  - Proper handling of microphone permissions

- **Advanced Transcription & Translation**
  - High-quality transcription using OpenAI models
  - Neural machine translation

## Running the Application

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vocallocal.git
   cd vocallocal
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   SECRET_KEY=some_random_secret_string
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open a web browser and go to:
   ```
   https://localhost:5000
   ```
   (Note: You'll need to accept the self-signed certificate warning)

## Using the Application

1. **Select Languages**
   - Each participant selects their language from the dropdown menu

2. **Start Conversation**
   - Click the microphone button to start recording
   - Speak clearly into your microphone
   - Click again to stop recording

3. **View Transcriptions and Translations**
   - Your original speech appears in the top box
   - The translation of your partner's speech appears in the bottom box

4. **Text-to-Speech**
   - Toggle the "Read translations aloud" option to have translations read to you

## Technical Implementation

- **Backend**: Flask web server with OpenAI API integration
- **Frontend**: HTML/CSS/JavaScript with Bootstrap for styling
- **Audio Processing**: Browser's MediaRecorder API
- **Speech Recognition**: OpenAI GPT-4o Transcribe models
- **Translation**: OpenAI GPT-4o for neural machine translation
- **Text-to-Speech**: Browser's SpeechSynthesis API

## Browser Compatibility

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome  | Full    | Best performance |
| Firefox | Full    | Good compatibility |
| Safari  | Full    | Requires HTTPS for microphone access |
| Edge    | Full    | Good compatibility |
| iOS Safari | Full | Some audio recording limitations |
| Android Chrome | Full | Good compatibility |

## Deployment to Render

1. **Fork or clone this repository**

2. **Create a new Web Service on Render**
   - Sign up for a [Render](https://render.com/) account if you don't have one
   - Go to your Render dashboard and click "New +" > "Web Service"
   - Connect your GitHub repository
   - Name your service (e.g., "vocallocal")
   - Select "Python" as the Environment
   - Set the Build Command to:
     ```
     ./build.sh
     ```
   - Set the Start Command to:
     ```
     gunicorn app:app
     ```

3. **Add Environment Variables**
   - Add your `OPENAI_API_KEY` to the environment variables section
   - Add `SECRET_KEY` for Flask session security

4. **Deploy your service**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## Troubleshooting

### Microphone Access Issues

If you're experiencing microphone access problems:

1. **Browser permissions** - When first using the app, your browser will ask for microphone access. Make sure to click "Allow". If you accidentally denied permission:
   - **Chrome**: Click the lock/info icon in the address bar, then change the microphone setting to "Allow"
   - **Firefox**: Click the lock icon, go to "Permissions" and enable microphone access
   - **Safari**: Go to Safari Preferences > Websites > Microphone and allow access for the site

2. **HTTPS requirement** - Browsers require HTTPS for microphone access. When running locally:
   - With SSL: `flask run --cert=adhoc` (requires pyopenssl)
   - Without SSL: Use localhost (http://127.0.0.1:5000) which browsers treat as secure
   - Alternative: Use a secure tunnel like ngrok: `ngrok http 5000`

3. **Device permissions** - Ensure your computer's system settings allow browser access to the microphone:
   - **Windows**: Settings > Privacy > Microphone
   - **macOS**: System Preferences > Security & Privacy > Privacy > Microphone
   - **Linux**: Varies by distribution, check your sound settings

4. **Try a different browser** - If one browser doesn't work, try Chrome, Firefox, or Edge

## License

[MIT](https://choosealicense.com/licenses/mit/)