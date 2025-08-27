#imagen DESCARGA LA IMAGEN DE DOCKER A USAR
FROM python:3.11

#Establece el directorio de trabajo
WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py

ENV PYTHONUNBUFFERED=1

EXPOSE 5550

CMD ["python", "app.py"]