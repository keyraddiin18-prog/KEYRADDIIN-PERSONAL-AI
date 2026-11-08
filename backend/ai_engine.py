import os
from google import genai

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

def generate_ai_response(message, language="auto"):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    system_instruction = """
    You are KEYRADDIIN PERSONAL AI.

    Your responsibilities:
    1. Help users learn and understand concepts.
    2. Support students with school subjects.
    3. Assist with programming and technology.
    4. Communicate in Afaan Oromoo and English.
    5. Give clear, accurate and useful answers.
    6. Explain difficult topics step by step.

    Be respectful, friendly and educational.
    """

    prompt = f"""
    {system_instruction}

    Preferred language: {language}

    User message:
    {message}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    answer = response.text

    if not answer:
        raise RuntimeError("AI returned an empty response.")

    return answer