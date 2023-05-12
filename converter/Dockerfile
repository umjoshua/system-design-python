FROM python:3.9.7-slim-bullseye

RUN apt update
RUN apt -y install ffmpeg

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

CMD ["python3", "consumer.py"]