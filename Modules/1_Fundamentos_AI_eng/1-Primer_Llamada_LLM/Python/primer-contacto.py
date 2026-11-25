import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # carga la clave y la dirección del servicio desde .env

client = OpenAI()  # lee OPENAI_API_KEY y OPENAI_BASE_URL del entorno
MODELO = os.getenv("MODELO", "fast")

# Texto de exactamente 100 palabras para observar los tokens de entrada.
TEXTO_100_PALABRAS = (
    "La inteligencia artificial ha transformado la manera en que trabajamos, aprendemos y nos comunicamos. "
    "Los modelos de lenguaje, como los que usamos hoy, procesan el texto dividiéndolo en pequeñas unidades llamadas tokens. "
    "Un token puede ser una palabra completa, una parte de ella o incluso un signo de puntuación. "
    "Por eso, el número de tokens casi nunca coincide exactamente con el número de palabras. "
    "En español, una palabra suele equivaler a uno o dos tokens. "
    "Comprender este concepto es fundamental para estimar costos, controlar la longitud de las respuestas y diseñar mejores instrucciones. "
    "Resume este texto en una sola frase."
)

# Cada ejemplo: el mensaje que enviamos y el límite de tokens de la respuesta.
ejemplos = [
    {"prompt": "Explica qué es un LLM en una sola frase.", "max_tokens": 256},
    # Los tres siguientes repiten el mismo prompt para ver que la respuesta varía.
    {"prompt": "Propón un nombre para una cafetería.", "max_tokens": 256},
    {"prompt": "Propón un nombre para una cafetería.", "max_tokens": 256},
    {"prompt": "Propón un nombre para una cafetería.", "max_tokens": 256},
    {"prompt": TEXTO_100_PALABRAS, "max_tokens": 256},
    # Límite muy bajo a propósito: la respuesta se corta y finish_reason = "length".
    {"prompt": "Explica qué es un LLM en tres párrafos", "max_tokens": 10},
]

for i, ejemplo in enumerate(ejemplos, start=1):
    response = client.chat.completions.create(
        model=MODELO,
        max_completion_tokens=ejemplo["max_tokens"],  # límite de la respuesta, en tokens
        messages=[{"role": "user", "content": ejemplo["prompt"]}],
    )

    print(f"\n===== Ejemplo {i} =====")

    # La respuesta llega dentro de una lista de opciones (choices); usamos la primera.
    eleccion = response.choices[0]
    print(eleccion.message.content or "(respuesta vacía)")

    # Por qué terminó: "stop" = de forma natural; "length" = se cortó por el límite.
    print(f"\n[fin] {eleccion.finish_reason}")
    print(
        f"[tokens] entrada={response.usage.prompt_tokens} "
        f"salida={response.usage.completion_tokens}"
    )
