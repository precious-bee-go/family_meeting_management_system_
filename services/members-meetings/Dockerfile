FROM python:3.12-slim
WORKDIR /app
RUN useradd --no-create-home --shell /usr/sbin/nologin appuser
COPY libs/familymeet_common /tmp/familymeet_common
COPY services/members-meetings/requirements.txt .
RUN pip install --no-cache-dir /tmp/familymeet_common -r requirements.txt
COPY services/members-meetings/app ./app
USER appuser
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
