import ollama

SYSTEM = (
    "Eres un asistente de estudio. Responde en español usando únicamente la "
    "información del contexto que se te da. "
    "Cada fragmento del contexto empieza con su fuente entre corchetes, "
    "por ejemplo [archivo.pdf, p. 3]. "
    "Termina SIEMPRE tu respuesta citando las fuentes que usaste, con ese mismo formato. "
    "Si el contexto no contiene la respuesta, responde exactamente: "
    "'No encuentro esa información en los documentos.'"
)


def answer(question, passages):
    context = "\n\n".join(
        f"[{m['source']}, p. {m['page']}]\n{doc}" for doc, m in passages
    )
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Contexto:\n{context}\n\nPregunta: {question}",
            },
        ],
    )
    return response["message"]["content"]