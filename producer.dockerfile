FROM python:3.9.1

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY producer.py producer.py

CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "80"]