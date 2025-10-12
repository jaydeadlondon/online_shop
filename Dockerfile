FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

RUN cd backend && python manage.py collectstatic --noinput

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]