FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS production

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} \
    && useradd -m -r -g ${APP_USER} ${APP_USER}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/${APP_USER}/.local/bin:${PATH}"

WORKDIR /app

COPY --from=builder /root/.local /home/${APP_USER}/.local

COPY . /app

RUN chown -R ${APP_USER}:${APP_USER} /app

USER ${APP_USER}

EXPOSE 80

CMD ["uvicorn", "microservice.main:app", "--host", "0.0.0.0", "--port", "80"]
