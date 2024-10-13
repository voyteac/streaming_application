FROM python:3.11.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y docker.io

RUN curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
