from fastapi import FastAPI, UploadFile, File
import shutil
import os

# AQUI ESTÁ O SEGREDO: Importamos sua função pronta!
from inteligencia import analisar_imagem_agora 

app = FastAPI()

@app.post("/analisar")
async def api_analisar(arquivo: UploadFile = File(...)):
    # 1. Salva o arquivo que chegou via internet num temp
    nome_temp = f"temp_{arquivo.filename}"
    
    with open(nome_temp, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    
    # 2. Chama a SUA inteligência que já estava pronta
    # Ela vai fazer o OCR, chamar o Gemini e devolver o resultado
    resultado = analisar_imagem_agora(nome_temp)
    
    # 3. Limpa a sujeira (apaga a imagem temp)
    os.remove(nome_temp)
    
    # 4. Devolve o resultado para o cliente (main.py ou app)
    return resultado