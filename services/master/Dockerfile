FROM python:3.9-slim

WORKDIR /app

# Install shared library
COPY shared /shared
RUN pip install /shared

COPY services/master/requirements.txt .
RUN pip install -r requirements.txt

COPY services/master/src/ src/

CMD ["python", "-u", "src/main.py"]
