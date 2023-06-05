# Utilizar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar los archivos de la aplicación al directorio de trabajo
COPY . .

# Exponer el puerto en el que se ejecuta la aplicación Flask
EXPOSE 5000

# Establecer el comando de inicio para ejecutar la aplicación
CMD ["python", "app.py"]