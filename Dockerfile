# Use a imagem oficial do Python como imagem base
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o container
COPY . .

# Exponha a porta 8000
EXPOSE 8000
