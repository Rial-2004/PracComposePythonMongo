# Usa una imagen base de Python oficial
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia el archivo de requisitos e instala las dependencias
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu aplicación
COPY app/ .

# El comando para iniciar la aplicación (ejemplo: usando gunicorn o python)
CMD ["python", "main.py"]