FROM python:3.9.1

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only consumer

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY consumer.py consumer.py

CMD ["python", "consumer.py"]