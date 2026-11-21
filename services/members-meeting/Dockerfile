# --STAGE 1 BUILD (INSTALL PACKAGES INTO / INSTALL)--
FROM python:3.12-slim AS builder
WORKDIR /build

COPY /lib/familymeet_common ./familymeet_common
COPY /services/members-meeting/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --prefix=/install ./familymeet_common -r requirements.txt

# --STAGE 2 RUN (SMALL FINAL IMAGE)--
COPY --from=builder /install /usr/local
COPY chown=appuser:appuser /services/members-meeting/app ./app/

USER appuser
EXPOSE 8004
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]
