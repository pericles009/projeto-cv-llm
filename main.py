import cv2
from ultralytics import YOLO
import os
import time
import requests # <--- ADICIONADO: Necessário para falar com a API

# --- REMOVIDO: from inteligencia import ... 
# Não importamos mais a inteligência aqui, pois ela roda no servidor (api.py)

# Cria pastas para organizar
os.makedirs('resultados/recortes', exist_ok=True)

print("Carregando modelo YOLO (Visão)... aguarde.")
model = YOLO('yolov8m.pt') 
print('Modelo carregado com sucesso!')

def read_image():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    print('\n--- SISTEMA CLIENTE INICIADO ---')
    print('📷 Aponte para o produto.')
    print('📡 O processamento será feito pela API.')
    print('🔘 Pressione "ESPAÇO" para enviar.')
    print('❌ Pressione "q" para SAIR.\n')

    while True:
        success, frame = cap.read()
        if not success:
            print('Falha ao capturar imagem.')
            break

        # Faz a detecção
        results = model.predict(frame, conf=0.5, verbose=False)

        frame_anotado = frame.copy() 
        recorte_atual = None

        # Loop por cada detecção
        for box in results[0].boxes:
            classe_id = int(box.cls[0])
            name = model.names[classe_id]
            
            # Filtro de pessoas
            if name == 'person':
                continue

            confianca = float(box.conf[0])

            if confianca > 0.6:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Desenha o retângulo
                cv2.rectangle(frame_anotado, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                texto = f"{name.upper()} {confianca:.2f}"
                cv2.putText(frame_anotado, texto, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Prepara o recorte com limites seguros
                h, w, _ = frame.shape
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                recorte_atual = frame[y1:y2, x1:x2]
                
                cv2.putText(frame_anotado, "PRODUTO DETECTADO! (Espaco para Enviar)", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Camera Cliente", frame_anotado)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == 32: # ESPAÇO
            if recorte_atual is not None:
                # Salva temporariamente para envio
                nome_arquivo = "temp_envio.jpg"
                cv2.imwrite(nome_arquivo, recorte_atual)
                
                print("📡 Enviando imagem para a API...")                
                
                try:
                    url = "http://127.0.0.1:8000/analisar"
                    
                    # CORREÇÃO DO ARQUIVO ABERTO:
                    # Usamos 'with open' para garantir que o arquivo feche após o envio
                    with open(nome_arquivo, 'rb') as f:
                        arquivos = {'arquivo': f}
                        resposta = requests.post(url, files=arquivos)
                    
                    # Agora o arquivo já está fechado, o código pode continuar
                    
                    if resposta.status_code == 200:
                        dados = resposta.json()
                        
                        # Verifica se dados não veio vazio
                        if dados: 
                            print("\n" + "="*40)
                            print(f"📖 Texto Lido: {dados.get('texto_lido')}")
                            print(f"🤖 Análise IA: {dados.get('analise_ia')}")
                            print("="*40 + "\n")
                        else:
                            print("⚠️ A API retornou dados vazios.")
                    else:
                        print(f"❌ Erro na API: {resposta.status_code}")
                    
                except Exception as e:
                    print(f"❌ Erro: {e}")

                # Agora sim pode deletar, pois o 'with open' já fechou o arquivo
                if os.path.exists(nome_arquivo):
                    try:
                        os.remove(nome_arquivo)
                    except:
                        pass # Se não der pra deletar, tudo bem, ele sobrescreve na próxima
            else:
                print("⚠️ Nada detectado para enviar.")

    cap.release()
    cv2.destroyAllWindows()
    # Limpa o arquivo temporário ao sair, se existir
    if os.path.exists("temp_envio.jpg"):
        os.remove("temp_envio.jpg")
    print("Programa encerrado.")

if __name__ == "__main__":
    read_image()