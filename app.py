from flask import Flask, request, jsonify, render_template, send_file
from gtts import gTTS
import os
from googletrans import Translator
from Scripts.ocr import img_2_text
import speech_recognition as sr

app = Flask(__name__, template_folder='templates')

if not os.path.exists('static'):
    os.makedirs('static')

if not os.path.exists('uploads'):
    os.makedirs('uploads')


def voice_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Error connecting to Google Speech Recognition service: {e}")

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/languages')
def get_languages():
    return jsonify({'languages': LANGUAGES})

@app.route('/translate', methods=['GET'])
def translate_text():
    try:
        text = request.args.get('text', '')
        from_lang = request.args.get('from_lang', 'iw')
        to_lang = request.args.get('to_lang', 'en')

        translator = Translator()
        translated_text = translator.translate(text, src=from_lang, dest=to_lang).text

        tts = gTTS(text=translated_text, lang=to_lang, slow=False)
        tts.save("static/output.mp3")

        return jsonify(
            {'original_text': text, 'translated_text': translated_text, 'from_lang': from_lang, 'to_lang': to_lang,
             'audio_file': 'output.mp3'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_audio')
def get_audio():
    return send_file('static/output.mp3', as_attachment=True, mimetype="audio/mpeg")

@app.route('/upload', methods=['POST'])
def upload_file():
    text = ''
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if uploaded_file and (uploaded_file.filename.endswith('.txt') or uploaded_file.filename.endswith('.png')):
            file_path = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(file_path)

            if uploaded_file.filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            elif uploaded_file.filename.endswith('.png'):
                text = img_2_text(file_path)

            translator = Translator()
            translated_text = translator.translate(text, src='en', dest=request.form['to_lang']).text
            translated_file_path = os.path.join('uploads', f'translated_{uploaded_file.filename}')
            with open(translated_file_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)

            return jsonify({
                'original_text': text,
                'translated_text': translated_text,
                'from_lang': 'en',
                'to_lang': request.form['to_lang'],
                'translated_file_path': translated_file_path
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
