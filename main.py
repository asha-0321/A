import streamlit as st
from googletrans import Translator as GoogleTranslator
from gtts import gTTS
import os
import base64
from docx import Document

language_mapping = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
    "bn": "Bengali",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "ar": "Arabic",
    "th": "Thai",
    "tr": "Turkish",
    "pl": "Polish",
    "cs": "Czech",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "el": "Greek",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "no": "Norwegian",
    "id": "Indonesian",
    "vi": "Vietnamese",
    "ro": "Romanian",
    "fa": "Persian",
    "iw": "Hebrew",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "hr": "Croatian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "is": "Icelandic",
    "ga": "Irish",
    "sq": "Albanian",
    "mk": "Macedonian",
    "hy": "Armenian",
    "ka": "Georgian",
    "ne": "Nepali",
    "si": "Sinhala",
    "km": "Khmer",
    "jw": "Javanese"
}

def translate_text_with_google(text, target_language):
    google_translator = GoogleTranslator()
    max_chunk_length = 500
    translated_text = ""
    for i in range(0, len(text), max_chunk_length):
        chunk = text[i:i + max_chunk_length]
        translated_chunk = google_translator.translate(chunk, dest=target_language).text
        translated_text += translated_chunk
    return translated_text

def convert_text_to_speech(text, output_file, language='en'):
    if text:
        supported_languages = list(language_mapping.keys())
        if language not in supported_languages:
            st.warning(f"Unsupported language: {language}")
            return
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)

def get_binary_file_downloader_html(link_text, file_path, file_format):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    b64_file = base64.b64encode(file_data).decode()
    download_link = f'<a href="data:{file_format};base64,{b64_file}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return download_link

def convert_text_to_word_doc(text, output_file):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_file)

def translate_text_with_fallback(text, target_language):
    try:
        return translate_text_with_google(text, target_language)
    except Exception as e:
        st.warning(f"Google Translate error: {str(e)}")
        return ""

def count_words(text):
    words = text.split()
    return len(words)

def main():
    st.image("jangirii.png", width=300)
    st.title("Text Translation and Conversion to Speech (MultiLingual)")

    text = st.text_area("Enter text to translate and convert to speech:", height=300)

    word_count = count_words(text)
    st.subheader(f"Word Count: {word_count} words")

    target_language = st.selectbox("Select target language:", list(language_mapping.values()))

    if st.button("Translate - Convert to Speech and get Translated document"):
        target_language_code = [code for code, lang in language_mapping.items() if lang == target_language][0]

        translated_text = translate_text_with_fallback(text, target_language_code)

        if translated_text:
            st.subheader(f"Translated text ({target_language}):
