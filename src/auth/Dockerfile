FROM python

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --no-cache-dir --requirement ./requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3","server.py"]