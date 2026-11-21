# --STAGE 1 BUILD (INSTALL PACKAGES INTO / INSTALL)--
FROM python:3.12-slim AS builder
WORKDIR /build

COPY /lib/familymeet_common ./familymeet_common
COPY /services/treasury/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --prefix=/install ./familymeet_common -r requirements.txt

# --STAGE 2 RUN (SMALL FINAL IMAGE)--
COPY --from=builder /install /usr/local
COPY chown=appuser:appuser /services/treasury/app ./app/

USER appuser
EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
