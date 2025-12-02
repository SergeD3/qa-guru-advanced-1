
FROM python:3.11

WORKDIR app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* README.md /app/

RUN poetry install --no-root

COPY . /app

CMD ["fastapi", "run", "src/app/main.py", "--port", "80"]
