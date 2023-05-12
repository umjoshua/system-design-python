FROM python:3.10.11-alpine3.18

RUN apk update
RUN apk add ffmpeg

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

CMD ["python3", "consumer.py"]