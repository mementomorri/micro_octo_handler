FROM python:3.11-slim

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2197"]


# Команда для запуска:
# docker build . --tag free_provider && docker run -p 2197:2197 free_provider
