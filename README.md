# 🌤️ Climbot – Multilingual Voice Weather Chatbot

**Climbot** is a multilingual AI-powered voice chatbot that provides accurate weather updates using [WeatherAPI.com](https://www.weatherapi.com/) and handles casual chat using OpenRouter AI (Google Gemma). It supports **English, Tamil, Hindi, and Telugu** and works via voice or text input.

---

## 🌍 Features

- 🎙️ **Voice & Text Input** (SpeechRecognition + gTTS)
- 🌐 **Multilingual**: Tamil, Hindi, Telugu, English
- ☀️ **Real-time weather** from [WeatherAPI](https://weatherapi.com/)
- 🧠 **Casual conversation** using `google/gemma-3-27b-it` via OpenRouter
- 🤖 Clean text output + audio response
- 🔄 **Translation layer** ensures correct weather classification
- 💾 Saves chat history for training/future logs

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io) – UI + deployment
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – Voice input
- [gTTS](https://pypi.org/project/gTTS/) + [Pygame](https://pypi.org/project/pygame/) – TTS playback
- [WeatherAPI.com](https://www.weatherapi.com/) – Weather data
- [OpenRouter](https://openrouter.ai) – LLM for casual responses
- [Deep Translator](https://pypi.org/project/deep-translator/) – Language translation
- `dotenv` – API key management

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/climbot-weather-chatbot.git
cd climbot-weather-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file:

```
WEATHER_API_KEY=your_weatherapi_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

✅ Or use **Streamlit secrets** / Render `render.yaml` instead for production.

---

## 🟢 Run Locally

```bash
streamlit run app.py
```

---

## 🌐 Deployment Options

### ✅ [Streamlit Cloud](https://streamlit.io/cloud)

- Push to GitHub
- Add secrets in Streamlit settings
- Set main file as `app.py`

### ✅ [Render.com](https://render.com)

- Use `render.yaml` (included)
- Add secrets in dashboard
- Auto-deploy from GitHub

---

## 🧪 Example Prompts

| Language | Prompt                                  |
|----------|------------------------------------------|
| English  | Will it rain in Chennai today?           |
| Tamil    | சென்னையில் இன்று மழை பெய்யுமா?             |
| Hindi    | क्या आज दिल्ली में बारिश होगी?            |
| Telugu   | హైదరాబాద్‌లో వాతావరణం ఎలా ఉంది?          |

---

## 📦 Project Structure

```
climbot-weather-chatbot/
├── app.py                 # Main app file
├── requirements.txt       # Dependencies
├── .env                   # Local API keys (not committed)
├── render.yaml            # Render deploy config (optional)
└── README.md              # You're reading this
```

---

## 📜 License

MIT License

---

## 🤝 Acknowledgements

- [OpenRouter](https://openrouter.ai/)
- [WeatherAPI](https://www.weatherapi.com/)
- [Streamlit](https://streamlit.io/)
```
