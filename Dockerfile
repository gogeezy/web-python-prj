# ---------- Base ----------
FROM python:3.14-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1


# ---------- Lint ----------
FROM base AS lint

RUN pip install --no-cache-dir ruff

COPY app.py .
COPY controllers ./controllers
COPY tests ./tests

RUN ruff check . > /tmp/lint-report.txt 2>&1 \
    && cat /tmp/lint-report.txt


# ---------- Test ----------
FROM base AS test

COPY app.py .
COPY controllers ./controllers
COPY tests ./tests

RUN pytest -v --junitxml=/tmp/pytest-report.xml


# ---------- Builder ----------
FROM base AS builder

COPY app.py .
COPY controllers ./controllers

RUN python -m compileall -b app.py controllers \
    && find . -type f -name '*.py' -delete \
    && find . -type d -name '__pycache__' -prune -exec rm -rf {} +


# ---------- Runtime ----------
FROM python:3.14-slim AS runtime

RUN useradd --create-home --uid 10001 appuser

WORKDIR /app

COPY --from=base /opt/venv /opt/venv
COPY --from=builder /app/app.pyc ./app.pyc
COPY --from=builder /app/controllers ./controllers

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 5000

ENTRYPOINT ["python", "app.pyc"]
