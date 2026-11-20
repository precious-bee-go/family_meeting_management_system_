FROM python:3.12-slim
WORKDIR /app
RUN useradd --no-create-home --shell /usr/sbin/nologin/ appuser
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
USER appuser