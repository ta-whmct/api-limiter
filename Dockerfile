FROM python:3.13.14-slim

RUN groupadd -r -g 1001 appgroup && \ 
    useradd -r -u 1001 -g appgroup -s /sbin/nologin appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser:appgroup

CMD ["python3", "run.py"]