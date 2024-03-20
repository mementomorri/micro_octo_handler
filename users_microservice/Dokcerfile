FROM python:3.11-slim

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# Команда для запуска:
# docker build . --tag users_microservice && docker run -p 80:80 users_microservice
