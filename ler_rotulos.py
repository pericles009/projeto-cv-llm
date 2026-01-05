import google.generativeai as genai

CHAVE_API = " " # chave API
genai.configure(api_key=CHAVE_API)

print("Listando modelos disponíveis...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erro: {e}")
