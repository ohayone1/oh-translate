## Multilingual Translation and Text-to-Speech Web App

This Flask web application provides translation services between multiple languages and also includes text-to-speech capabilities. Users can either input text or upload a text file or an image with text to be translated. The translated text is then converted to speech and can be downloaded as an MP3 file.

### Features:

- Translate text from one language to another.
- Convert translated text to speech and download as an MP3 file.
- Upload a text file or an image with text for translation.

### Technologies Used:

- **Flask**: Python web framework used for backend development.
- **gTTS**: Google Text-to-Speech for converting text to speech.
- **googletrans**: Google Translate API for language translation.
- **SpeechRecognition**: For converting speech to text.
- **OCR**: Optical Character Recognition to extract text from images.

### Setup:

1. Clone the repository:

    ```bash
    git clone https://github.com/ohayone1/oh-translate.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python app.py
    ```

### API Endpoints:

- **GET /**: Home page, renders `index.html`.
  
- **GET /languages**: Get a list of supported languages.

    **Example**: `http://localhost:5000/languages`

- **GET /translate**: Translate text.

    **Parameters**:
    - `text`: Text to be translated.
    - `from_lang`: Source language (default is 'iw').
    - `to_lang`: Target language (default is 'en').

    **Example**: `http://localhost:5000/translate?text=hello&from_lang=en&to_lang=es`

- **GET /get_audio**: Download the translated text as an MP3 file.

    **Example**: `http://localhost:5000/get_audio`

- **POST /upload**: Upload a text file or an image with text for translation.

    **Form Data**:
    - `file`: Text file or image file.
    - `to_lang`: Target language for translation.

    **Example**: `http://localhost:5000/upload`

### Directory Structure:

```
.
├── app.py
├── templates
│   └── index.html
├── Scripts
│   └── ocr.py
├── static
│   └── output.mp3
└── uploads
    └── uploaded_file.txt
```

### Supported Languages:

The application supports translation between the following languages:

```python
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    ...
    'zu': 'zulu'
}
```

### Note:

- Ensure the `static` and `uploads` directories exist before running the application.

### Contributors:

- [ohayone1](https://github.com/ohayone1)

Feel free to contribute to this project by submitting issues or pull requests!
