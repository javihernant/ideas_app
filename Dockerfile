FROM python:3

# Configure Poetry
ENV POETRY_VENV=/opt/poetry-venv

# Install poetry
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /ideas_app


COPY . .
# Install dependencies
RUN poetry install