# 1. Imagem base
FROM python:3.10-slim

# 2. Configurações para evitar logs presos e arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta de trabalho
WORKDIR /app

# 4. INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA (CRUCIAL PARA EASYOCR/OPENCV)
# O "libgl1" e "libglib2.0" são obrigatórios para processamento de imagem
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# 5. Copia e instala as bibliotecas Python
COPY requirements.txt .
# A flag --timeout aumenta o tempo limite, pois o PyTorch é grande e pode demorar para baixar
RUN pip install --no-cache-dir -r requirements.txt --timeout 1000

# 6. Copia o código da API
COPY . .

# 7. O Google Cloud Run precisa salvar os modelos do EasyOCR em algum lugar
# Criamos uma pasta para ele e damos permissão
RUN mkdir -p /root/.EasyOCR

# 8. Expõe a porta e roda o Uvicorn
EXPOSE 8080
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]