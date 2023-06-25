# syntax=docker/dockerfile:1

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install "poetry==1.5.1"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

# create dummy .env file so django-configurations
# loads settings properly
RUN touch /app/.env

EXPOSE 8000

CMD ["python", "manage.py" , "runserver", "0.0.0.0:8000"]