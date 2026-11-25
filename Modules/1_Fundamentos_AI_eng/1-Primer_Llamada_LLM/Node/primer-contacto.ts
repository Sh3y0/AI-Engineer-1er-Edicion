import "dotenv/config"; // carga la clave y la dirección del servicio desde .env
import OpenAI from "openai";

const client = new OpenAI(); // lee OPENAI_API_KEY y OPENAI_BASE_URL del entorno
const MODELO = process.env.MODELO ?? "fast";

// Texto de exactamente 100 palabras para observar los tokens de entrada.
const TEXTO_100_PALABRAS =
    "La inteligencia artificial ha transformado la manera en que trabajamos, aprendemos y nos comunicamos. " +
    "Los modelos de lenguaje, como los que usamos hoy, procesan el texto dividiéndolo en pequeñas unidades llamadas tokens. " +
    "Un token puede ser una palabra completa, una parte de ella o incluso un signo de puntuación. " +
    "Por eso, el número de tokens casi nunca coincide exactamente con el número de palabras. " +
    "En español, una palabra suele equivaler a uno o dos tokens. " +
    "Comprender este concepto es fundamental para estimar costos, controlar la longitud de las respuestas y diseñar mejores instrucciones. " +
    "Resume este texto en una sola frase.";

// Cada ejemplo: el mensaje que enviamos y el límite de tokens de la respuesta.
const ejemplos = [
    { prompt: "Explica qué es un LLM en una sola frase.", maxTokens: 256 },
    // Los tres siguientes repiten el mismo prompt para ver que la respuesta varía.
    { prompt: "Propón un nombre para una cafetería.", maxTokens: 256 },
    { prompt: "Propón un nombre para una cafetería.", maxTokens: 256 },
    { prompt: "Propón un nombre para una cafetería.", maxTokens: 256 },
    { prompt: TEXTO_100_PALABRAS, maxTokens: 256 },
    // Límite muy bajo a propósito: la respuesta se corta y finish_reason = "length".
    { prompt: "Explica qué es un LLM en tres párrafos", maxTokens: 10 },
];

for (const [i, ejemplo] of ejemplos.entries()) {
    const response = await client.chat.completions.create({
        model: MODELO,
        max_completion_tokens: ejemplo.maxTokens, // límite de la respuesta, en tokens
        messages: [{ role: "user", content: ejemplo.prompt }],
    });

    console.log(`\n===== Ejemplo ${i + 1} =====`);

    // La respuesta llega dentro de una lista de opciones (choices); usamos la primera.
    const eleccion = response.choices[0];
    console.log(eleccion.message.content || "(respuesta vacía)");

    // Por qué terminó: "stop" = de forma natural; "length" = se cortó por el límite.
    console.log(`\n[fin] ${eleccion.finish_reason}`);
    console.log(
        `[tokens] entrada=${response.usage?.prompt_tokens} salida=${response.usage?.completion_tokens}`,
    );
}
