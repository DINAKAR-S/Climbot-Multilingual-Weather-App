import streamlit as st
import requests
import wavio
import sounddevice as sd
import speech_recognition as sr
import openai
import os
import uuid
import json
import time
import re
import pygame
from gtts import gTTS
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load API keys
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter Setup
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# Streamlit config
st.set_page_config(page_title="🌤️ Climbot – Multilingual Weather Chat")

# Session state
if 'recent_cities' not in st.session_state:
    st.session_state.recent_cities = []
if 'conversation_log' not in st.session_state:
    st.session_state.conversation_log = []

# Languages supported
languages = {
    "English": {"rec": "en-IN", "tts": "en", "trans": "en"},
    "Tamil": {"rec": "ta-IN", "tts": "ta", "trans": "ta"},
    "Hindi": {"rec": "hi-IN", "tts": "hi", "trans": "hi"},
    "Telugu": {"rec": "te-IN", "tts": "te", "trans": "te"}
}

lang_choice = st.selectbox("🌐 Choose your language", list(languages.keys()))
rec_lang = languages[lang_choice]["rec"]
tts_lang = languages[lang_choice]["tts"]
trans_lang = languages[lang_choice]["trans"]

weather_translations = {
    "English": "{} in {}, {} with temperature {}°C.",
    "Tamil": "{} நிலைமை, {}, {} பகுதியில். வெப்பநிலை: {}°C.",
    "Hindi": "{} की स्थिति {}, {} में है। तापमान: {}°C.",
    "Telugu": "{} ఉంది, {}, {} ప్రాంతంలో ఉంది. ఉష్ణోగ్రత: {}°C."
}


# City list (expandable)
city_keywords = [
    "chennai", "delhi", "mumbai", "kolkata", "bangalore", "hyderabad", "pune", "coimbatore", "madurai",
    "tirunelveli", "trichy", "vellore", "hosur", "salem", "ahmedabad", "lucknow", "patna",
    "vizag", "tirupati",
    "சென்னை", "மதுரை", "கோயம்புத்தூர்", "திருச்சி",
    "दिल्ली", "मुंबई", "लखनऊ", "पटना", "कोलकाता",
    "హైదరాబాద్", "చెన్నై", "తిరుపతి", "ముంబై"
]

def clean_response(text):
    return re.sub(r"[*_~`]", "", text)

def speak(text, lang='en'):
    tts = gTTS(text=clean_response(text), lang=lang)
    filename = f"{uuid.uuid4()}.mp3"
    tts.save(filename)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(filename)

def record_audio(filename="input.wav", duration=5, fs=44100):
    st.info("🎙️ Recording... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, audio, fs, sampwidth=2)

def recognize_audio(file_path="input.wav", lang='en-IN'):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
        try:
            return r.recognize_google(audio, language=lang)
        except:
            return None

def translate_to_english(text, source_lang):
    try:
        return GoogleTranslator(source=source_lang, target='en').translate(text)
    except:
        return text

def is_weather_query(text):
    keywords = ["weather", "rain", "temperature", "cold", "hot", "forecast", "sunny", "cloud",
                "மழை", "வானிலை", "வெப்பம்", "சூடாக", "குளிர்",
                "वर्षा", "मौसम", "ठंड", "गर्मी",
                "వాతావరణం", "వర్షం", "చలి", "వేడి"]
    return any(word in text.lower() for word in keywords)

def contains_city(text):
    text = text.lower()
    return any(city.lower() in text for city in city_keywords)

def extract_location(text):
    match = re.search(r"(in|at|for|of)\s+([A-Za-z\s]+)", text)
    if match:
        return match.group(2).strip() + ", India"
    else:
        return text + ", India"  # Fallback

def get_weather(city, lang='English'):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    res = requests.get(url)
    data = res.json()

    if "error" in data:
        return {
            "English": "⚠️ Couldn't find that location.",
            "Tamil": "⚠️ அந்த இடத்தை கண்டுபிடிக்க முடியவில்லை.",
            "Hindi": "⚠️ स्थान नहीं मिला।",
            "Telugu": "⚠️ ఆ ప్రదేశాన్ని కనుగొనలేకపోయాం."
        }[lang]

    loc = data["location"]
    cur = data["current"]
    condition = cur["condition"]["text"]

    localized_conditions = {
        "Partly cloudy": {
            "Tamil": "பகுதி மேகமூட்டம்",
            "Hindi": "आंशिक रूप से बादल",
            "Telugu": "పాక్షికంగా మేఘావృతం"
        },
        "Sunny": {
            "Tamil": "வெயிலாக உள்ளது",
            "Hindi": "धूप है",
            "Telugu": "ఎండగా ఉంది"
        },
        "Cloudy": {
            "Tamil": "மேகமூட்டம்",
            "Hindi": "बादल छाए हुए हैं",
            "Telugu": "మేఘావృతం"
        },
        "Clear": {
            "Tamil": "வெளிச்சமான வானிலை",
            "Hindi": "साफ़ मौसम",
            "Telugu": "స్పష్టమైన వాతావరణం"
        }
        
    }

    localized_condition = localized_conditions.get(condition, {}).get(lang, condition)

    return weather_translations[lang].format(
    localized_condition,
    loc["name"],
    loc["region"],
    cur["temp_c"]
    )



def casual_reply(user_input):
    messages = [{"role": "user", "content": user_input}]
    res = openai.ChatCompletion.create(
        model="google/gemma-3-27b-it:free",
        messages=messages
    )
    return res["choices"][0]["message"]["content"]

def update_recent(city):
    if city not in st.session_state.recent_cities:
        st.session_state.recent_cities.insert(0, city)
    if len(st.session_state.recent_cities) > 5:
        st.session_state.recent_cities = st.session_state.recent_cities[:5]

# --- UI Starts ---
st.title("🌤️ Climbot – Multilingual Voice Weather & Chatbot")
use_voice = st.toggle("🎙️ Use voice input", value=True)
user_input = None

if use_voice:
    if st.button("🎙️ Start Recording"):
        record_audio()
        user_input = recognize_audio(lang=rec_lang)
        if not user_input:
            user_input = st.text_input("Couldn't hear. Please type 👇")
        else:
            st.success(f"🗣️ You said: {user_input}")
else:
    user_input = st.text_input("Type your question:")

if user_input:
    update_recent(user_input)

    # Translate to English
    translated_input = translate_to_english(user_input, trans_lang)

    # Weather intent detection
    if is_weather_query(translated_input) or contains_city(translated_input):
        location = extract_location(translated_input)
        response = get_weather(location, lang=lang_choice)
    else:
        response = casual_reply(user_input)

    cleaned = clean_response(response)
    st.write("🤖", cleaned)
    speak(cleaned, lang=tts_lang)
    st.session_state.conversation_log.append({"user": user_input, "bot": cleaned})

st.markdown("### 🕘 Recently Asked Cities")
for city in st.session_state.recent_cities:
    st.write(f"➡️ {city}")

# Export
if st.checkbox("💾 Save chat"):
    if st.button("Export"):
        with open("chat_log.json", "w") as f:
            json.dump(st.session_state.conversation_log, f, indent=2)
        st.success("Saved chat_log.json")

if st.checkbox("🧠 Save for training"):
    with open("training_data.txt", "a") as f:
        for entry in st.session_state.conversation_log:
            f.write(f"Q: {entry['user']}\nA: {entry['bot']}\n\n")
    st.success("Training data saved.")
