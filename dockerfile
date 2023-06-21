# syntax=docker/dockerfile:1

FROM python:3.10-alpine

RUN pip install "poetry==1.5.1"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

# create database tables and insert demo data
RUN python manage.py migrate \
    && python manage.py loadcsv \ 
    --csv catalogue/management/commands/init.csv \ 
    --image_folder product_images \
    --lorem_description True \
    && python manage.py loadcomments \ 
    --csv comments/management/commands/init.csv \ 
    --lorem_text True \
    && python manage.py loadarticles \ 
    --csv articles/management/commands/init.csv \
    --image_folder article_images

EXPOSE 8000

CMD ["python", "manage.py" , "runserver", "0.0.0.0:8000"]