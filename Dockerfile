FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws \
    && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "app.py"]