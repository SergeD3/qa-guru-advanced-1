
FROM python:3.11


WORKDIR /qa-guru-advanced-1


RUN pip install poetry


# COPY ./requirements.txt /code/requirements.txt
COPY pyproject.toml poetry.lock* README.md /qa-guru-advanced-1/


# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN poetry config virtualenvs.create false


RUN poetry install


COPY ./src /qa-guru-advanced-1/src


CMD ["fastapi", "run", "src/app/main.py", "--port", "80"]