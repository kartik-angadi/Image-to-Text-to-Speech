from flask import Flask, request, jsonify, send_file
import pytesseract
from PIL import Image
import pyttsx3
import tempfile
import os

app = Flask(__name__)

# Path to your Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_file):
    # Open the image file
    image = Image.open(image_file)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text


def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties before adding things to say
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio_path = temp_audio.name
        engine.save_to_file(text, temp_audio_path)
        engine.runAndWait()

    return temp_audio_path


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400

    image_file = request.files['image']
    extracted_text = extract_text_from_image(image_file)

    # Convert text to speech
    audio_file_path = text_to_speech(extracted_text)

    # Return the text and audio file path in the response
    return jsonify({'extracted_text': extracted_text, 'audio_file_path': audio_file_path})


@app.route('/audio/<path:path>')
def stream_audio(path):
    return send_file(path)


if __name__ == '__main__':
    app.run(debug=True)
