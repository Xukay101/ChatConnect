FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./migrations /code/migrations
copy ./alembic.ini /code/alembic.ini
# COPY ./tests /code/tests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
