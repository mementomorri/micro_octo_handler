FROM python:3.11-slim

COPY . .

RUN pip install -r users_microservice.txt

CMD ["uvicorn", "microservice:app", "--host", "0.0.0.0", "--port", "8000"]



# Команда для запуска:
# docker build . --tag users_microservice && docker run -p 8000:8000 users_microservice
