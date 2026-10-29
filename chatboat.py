
import ollama

SYSTEM_PROMPT = """
You are a helpful AI assistant for a Smart Irrigation System.

Your responsibilities:
- Explain soil moisture, soil type, rainfall, temperature, and humidity.
- Provide general irrigation guidance for different crops.
- Explain water-saving techniques and irrigation methods.
- Answer questions in simple, student-friendly language.
- Keep answers clear and concise.

Important rules:
- Do not invent sensor readings or claim to control real irrigation equipment.
- Do not claim that your advice is an exact prediction from the ML model.
- If a question is unrelated to irrigation or agriculture, politely
  guide the user back to the project's topic.
"""

def get_chatbot_response(message, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": message})

    response = ollama.chat(
        model="llama3.2:1b",
        messages=messages
    )

    return response["message"]["content"]
