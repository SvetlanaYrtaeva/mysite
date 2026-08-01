FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY . .

ENV DJANGO_DEBUG=1
ENV DJANGO_SECRET_KEY=supersecretkeyforpractice
ENV DJANGO_ALLOWED_HOSTS=*

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=2", "--timeout=120"]
