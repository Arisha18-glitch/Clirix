# Clirix — Your Thinking Layer

A fully local AI assistant that runs 100% on your machine. No API keys, no subscriptions, no data leaving your device.



## Screenshots
# Dasboard
<img width="975" height="464" alt="image" src="https://github.com/user-attachments/assets/392624eb-c473-4879-98fe-048920cf54b3" />
# Attached file
<img width="975" height="467" alt="image" src="https://github.com/user-attachments/assets/691307bc-4ede-4c7e-9ad4-ae752c944102" />
# Captured Audio
<img width="975" height="228" alt="image" src="https://github.com/user-attachments/assets/9c91e36a-1dc4-4a12-a96a-13b33f06b403" />
# rasponding
<img width="975" height="444" alt="image" src="https://github.com/user-attachments/assets/20935a0d-b60d-4bb9-9d2a-c22cd6b70294" />


## Features

- Streams responses word-by-word like ChatGPT via Ollama
- Full conversation history with context-aware replies
- Multi-model switching — Mistral, Phi-3, Gemma, or any Ollama model
- PDF document intelligence with custom RAG engine (700-word chunks, 80-word overlap)
- One-click voice input via Google STT that auto-fills the chat box
- 5 tone modes: Formal, Casual, ELI5, Bullets, Technical

## Tech Stack

- **Frontend:** Streamlit
- **LLM Backend:** Ollama (local inference)
- **Voice:** SpeechRecognition + Google STT
- **Document Parsing:** pdfplumber
- **State:** Streamlit Session State
## Ollama Setup

1. Download and install Ollama from https://ollama.com

2. Pull a model (Mistral recommended):
```bash
ollama pull mistral
```

3. Other supported models:
```bash
ollama pull phi3
ollama pull gemma
ollama pull llama3
```

4. Make sure Ollama is running before launching Clirix:
```bash
ollama serve
```

> Ollama runs locally on `http://localhost:11434` by default. Clirix connects to it automatically.

## Code Setup

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Privacy

100% local inference. The only external call is optional Google STT for voice input. No data is sent to any third-party LLM provider.
