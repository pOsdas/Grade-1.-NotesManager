FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1  # Отключить создание .pyc-файлов
ENV PYTHONUNBUFFERED 1        # Обеспечить немедленный вывод в консоль

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
