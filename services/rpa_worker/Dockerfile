FROM python:3.9-slim

WORKDIR /app

COPY shared /shared
RUN pip install /shared

COPY services/rpa_worker/src/ src/

CMD ["python", "-u", "src/main.py"]
