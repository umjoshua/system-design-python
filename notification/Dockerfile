FROM python:3.10.11-alpine3.18

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir --requirement ./requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python3","consumer.py"]