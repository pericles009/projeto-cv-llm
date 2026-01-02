import google.generativeai as genai
import easyocr
from dotenv import load_dotenv
import os
import cv2  # ADICIONE ESTA LINHA

# --- CONFIGURAÇÕES (Carregam apenas uma vez) ---
load_dotenv()
chave_api = os.getenv("GOOGLE_API_KEY") # <--- RECOLOQUE SUA CHAVE AQUI
genai.configure(api_key=chave_api)
model = genai.GenerativeModel('gemini-2.5-flash') 

print("Inicializando OCR e IA... (Isso acontece só uma vez)")
# Mantenha gpu=False se não tiver CUDA configurado
reader = easyocr.Reader(['pt', 'en'], gpu=False)

def analisar_imagem_agora(caminho_imagem):
    print(f"\n--- 🧠 INICIANDO ANÁLISE: {caminho_imagem} ---")

    # 1. OCR (LEITURA) - FORMA MAIS SEGURA
    try:
        print("Executando OCR...")
        # CORREÇÃO: Carregar e converter para escala de cinza
        img = cv2.imread(caminho_imagem)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    

        resultados_brutos = reader.readtext(img_gray)
        
        # Vamos extrair só o texto manualmente para não dar erro de desempacotamento
        lista_textos = []
        for item in resultados_brutos:
            # O formato do item é: ( [caixa], "texto lido", confiança )
            if len(item) >= 2:
                texto = item[1] 
                lista_textos.append(texto)
        texto_detectado = " ".join(lista_textos)
        print(f"📖 Texto Bruto: {texto_detectado}")

        if len(texto_detectado) < 2:
            print("⚠️ Pouco texto. A identificação pode falhar.")
            return 

    except Exception as e:
        print(f"Erro no OCR: {e}")
        return



    # 2. IA (INTERPRETAÇÃO)
    prompt = f"""
    Analise este texto de rótulo de produto: "{texto_detectado}"
    Identifique: Categoria | Marca | Detalhes.
    Responda apenas nesse formato e não escreva textos longos. Se não souber, diga "Não identificado".
    """

    try:
        response = model.generate_content(prompt)
        print(f"🤖 RESPOSTA IA: {response.text}") # Isso aparece no servidor (OK)
        
        # --- O SEGREDO ESTÁ AQUI: TEM QUE TER O RETURN ---
        return {
            "texto_lido": texto_detectado,
            "analise_ia": response.text
        }
        # -------------------------------------------------

    except Exception as e:
        print(f"Erro na IA: {e}")
        return {"texto_lido": "Erro", "analise_ia": "Erro na IA"}