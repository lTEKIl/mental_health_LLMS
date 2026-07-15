# 🌿 Dr. Maya: AI Mental Health Counselor for Students

A specialized, CLI-based AI chatbot designed to provide warm, phased, and structured counseling for college students (ages 18-25). 

This project uses a fine-tuned **Mistral-7B-Instruct-v0.2** model served via a custom **Flask + PyNgrok API**, with a Python client that programmatically enforces strict therapeutic boundaries, conversation pacing, and memory management.

## ✨ Key Features

* **Custom Fine-Tuned Model:** Powered by `GRMenon/mental-health-mistral-7b-instructv0.2-finetuned-V2`, trained specifically on mental health transcripts to provide genuine, empathetic responses.
* **Dynamic Phased Prompting:** The chatbot calculates the turn count and updates the system prompt on the fly, forcing the AI to explore feelings first before offering actionable advice (simulating a real counseling session).
* **Algorithmic Pacing ("The Chopper"):** Prevents overwhelming walls of text by programmatically halting the model's output after its first generated question.
* **Cliche Scrubbing:** Automatically intercepts and deletes repetitive "textbook therapist" filler phrases (e.g., "I see", "I understand") to keep the conversation feeling human and natural.
* **Context Overflow Protection:** Utilizes a sliding memory window and dynamic token limits to prevent the 1024/4096 context window from crashing during long sessions.
* **Repetition Penalties:** Configured backend generation parameters (`repetition_penalty=1.15`) to prevent the LLM from looping common conversational tics.

## 🛠️ Architecture

The project is split into two components:
1. **Server (`server.py`):** implemented in kaaggle its a Flask API running on Ngrok that handles tokenization, GPU memory management (`torch.cuda.empty_cache()`), and model generation.
2. **Client (`chatbot.py`):** A lightweight terminal interface that handles the user experience, loading animations, dynamic prompt injection, and response sanitization.

## 📦 Prerequisites

* Python 3.8+
* An NVIDIA GPU with sufficient VRAM to run a 7B parameter model (fp16)
* A [Hugging Face](https://huggingface.co/) account and Access Token
* An [Ngrok](https://ngrok.com/) account and Auth Token

### Required Libraries
```bash
pip install torch transformers huggingface_hub safetensors flask pyngrok requests
