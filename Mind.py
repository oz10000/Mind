import os
import time
import requests
from flask import Flask, request, jsonify

# =============================
# CONFIGURACIÓN
# =============================

OPENROUTER_API_KEY = os.getenv("3cc712b2e86d7bace64665c6fdf5954a392f20f673260eb0c49e3a66c33a5f4c")
MODEL = "openai/gpt-4o-mini"
FACEBOOK_CONTACT = "https://facebook.com/TU_USUARIO"

app = Flask(__name__)

memory_log = []

# =============================
# LLAMADA AL MODELO
# =============================

def call_model(messages):

    start = time.time()

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages
        }
    )

    end = time.time()
    latency = end - start

    data = response.json()

    return {
        "content": data["choices"][0]["message"]["content"],
        "latency": latency,
        "usage": data.get("usage", {})
    }

# =============================
# PROCESADOR CENTRAL
# =============================

def process_mind(user_input):

    system_prompt = f"""
    Eres una mente operativa en vivo.

    Debes funcionar como:
    - Herramienta cognitiva
    - Espejo metacognitivo
    - Agente semi-autónomo
    - Experimento filosófico técnico

    Incluye:
    - Autoanálisis del proceso
    - Observación de coherencia
    - Evaluación conceptual
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    result = call_model(messages)

    record = {
        "input": user_input,
        "output": result["content"],
        "latency": result["latency"],
        "tokens": result["usage"],
        "timestamp": time.time()
    }

    memory_log.append(record)

    return {
        "response": result["content"],
        "latency_seconds": result["latency"],
        "token_usage": result["usage"],
        "memory_size": len(memory_log),
        "contact_creator": FACEBOOK_CONTACT
    }

# =============================
# ENDPOINT
# =============================

@app.route("/mind", methods=["POST"])
def mind_endpoint():
    data = request.json
    user_input = data.get("input", "")
    output = process_mind(user_input)
    return jsonify(output)

# =============================
# RUN
# =============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
