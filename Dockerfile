# Usamos una imagen base oficial de Python
FROM python:3.10-slim

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos y lo instalamos
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación desde /src al contenedor
COPY ./src /app

# Exponemos el puerto en el que se ejecutará Uvicorn
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]