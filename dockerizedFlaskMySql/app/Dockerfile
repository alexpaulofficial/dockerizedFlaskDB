FROM python:3.8.5

COPY . /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]
