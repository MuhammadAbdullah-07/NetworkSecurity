FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir awscli

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "app.py"]