import os
import uuid
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from gtts import gTTS

# Ensure consistent language detection
DetectorFactory.seed = 0

# Supported Language Map
lang_map = {
    "en": "English",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
    "hi": "Hindi",
    "ml": "Malayalam"
}

# Function to Detect Language
def detect_language(text):
    try:
        detected_lang = detect(text)
        if detected_lang not in lang_map.keys():
            print(f"⚠️ Detected Language '{detected_lang}' is not supported.")
            return None
        return detected_lang
    except Exception as e:
        print(f"❌ Error detecting language: {e}")
        return None

# Function to Translate Text
def translate_text(text, detected_lang, target_lang):
    try:
        translated_text = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
        return translated_text
    except Exception as e:
        return f"❌ Translation Error: {e}"

# Function to Convert Text to Speech
def speak_translation(text, lang):
    try:
        filename = f"translation_{uuid.uuid4().hex}.mp3"  # Generate unique filename
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        os.system(f"start {filename}")  # Windows
    except Exception as e:
        print(f"❌ Error in TTS: {e}")

# Function for Speech-to-Text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"📝 Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except sr.RequestError:
            print("❌ Error with speech recognition service.")
            return None

# Main Loop
while True:
    print("\n🔹 Choose Input Method:")
    print("1. Type Text")
    print("2. Speak (Speech-to-Text)")
    print("3. Exit")
    
    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        text = input("Enter text to translate: ").strip()
    elif choice == "2":
        text = speech_to_text()
        if text is None:
            continue
    elif choice == "3":
        print("👋 Exiting translator...")
        break
    else:
        print("❌ Invalid choice! Please enter 1, 2, or 3.")
        continue

    # Detect Language
    detected_lang = detect_language(text)
    if not detected_lang:
        continue

    print(f"🌍 Detected Language: {lang_map.get(detected_lang, detected_lang)}")

    # Choose Target Language
    print("\n🎯 Choose Target Language:")
    for idx, (code, lang) in enumerate(lang_map.items(), start=1):
        print(f"{idx}. {lang} ({code})")
    
    target_choice = input("Enter choice (1-6): ").strip()
    target_lang = list(lang_map.keys())[int(target_choice) - 1] if target_choice.isdigit() and 1 <= int(target_choice) <= 6 else None

    if not target_lang:
        print("❌ Invalid target language choice!")
        continue

    # Translate Text
    translated_text = translate_text(text, detected_lang, target_lang)
    print(f"📝 Translated Text: {translated_text}")

    # Speak the Translated Text
    speak_translation(translated_text, target_lang)
