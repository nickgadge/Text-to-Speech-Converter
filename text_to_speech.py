from gtts import gTTS
import os
import sys
from datetime import datetime

def get_output_dir():
    """Get the absolute path to the audio output directory"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'audio')

def text_to_speech(text):
    output_dir = get_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"speech_{timestamp}.mp3"
    filepath = os.path.join(output_dir, filename)

    try:
        # Create TTS object and save to file
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filepath)

        # Verify file was created
        if os.path.exists(filepath):
            return filename
        return None
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return None

if __name__ == "__main__":
    try:
        text = sys.stdin.read().strip()
        if text:
            filename = text_to_speech(text)
            print(filename if filename else "ERROR", end='')
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)
