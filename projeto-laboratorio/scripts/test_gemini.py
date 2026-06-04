import os
from google import genai

try:
    print("Tentando inicializar o GenAI Client...")
    client = genai.Client()
    print("Cliente inicializado. Enviando requisição...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Olá, você está funcionando?',
    )
    print("Resposta do Gemini:")
    print(response.text)
except Exception as e:
    print(f"Erro ao usar a API do Gemini: {e}")
