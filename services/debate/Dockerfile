# -- STAGE 1 BUILDS (INSTALL THE PACKAGES) --
FROM python:3.12-slim AS builder
WORKDIR /build
COPY libs/familymeet_common ./familymeet_common
COPY services/debate/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install ./familymeet_common -r requirements.txt

# -- STAGE 2 RUN (SMALL FINAL IMAGE) --
FROM python:3.12-slim
WORKDIR /app
RUN useradd --no-create-home --shell /usr/sbin/nologin appuser
COPY services/debate/app ./app
USER appuser
EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]