import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
MODELO = os.getenv("MODELO", "fast")

response = client.chat.completions.create(
    model=MODELO,
    max_completion_tokens=256,
    messages=[
        {"role": "user", "content": "Explica qué es un LLM en una sola frase."}
    ]
)

eleccion = response.choices[0]
print(eleccion.message.content or "No se pudo generar la respuesta")

print(f"\n[fin] {eleccion.finish_reason}")
print(
    f"\n[token] entrada: {response.usage.completion_tokens}"
    f"\n[prompt] {response.usage.prompt_tokens}"
)