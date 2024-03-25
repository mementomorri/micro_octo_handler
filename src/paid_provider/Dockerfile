FROM python:3.11-slim

COPY . .

RUN pip install -r paid_provider.txt

CMD ["uvicorn", "provider:app", "--host", "0.0.0.0", "--port", "2198"]


# Команда для запуска:
# docker build . --tag paid_provider && docker run -p 2198:2198 paid_provider
