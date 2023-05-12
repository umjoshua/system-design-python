FROM python:3.9.7-slim-bullseye

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir --requirement ./requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python3","consumer.py"]