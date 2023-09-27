FROM python:3.11

#cria diretório de trabalho
WORKDIR /app

#copia arquivo de dependências para container e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copia restante do código para o container
COPY . .

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5001", "--reload"]

EXPOSE 5001