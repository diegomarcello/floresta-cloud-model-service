FROM python:3.9-slim

WORKDIR /app

COPY shared /shared
RUN pip install /shared

COPY services/monitor/src/ src/

CMD ["python", "-u", "src/main.py"]
