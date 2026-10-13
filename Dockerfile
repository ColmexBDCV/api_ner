# Usar una imagen base oficial de Python
FROM python:3.10-slim-bookworm

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar Java (OpenJDK 17) y otras dependencias
RUN apt-get update && apt-get install -y openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de la aplicación a la imagen
COPY . .

# Instalar las dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que la aplicación usará
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:8000"]
