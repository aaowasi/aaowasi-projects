FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY services/mcp-server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY engine /app/engine
COPY config /app/config
COPY data/source /app/data/source
COPY services/mcp-server/server.py /app/services/mcp-server/server.py
USER 65532:65532
ENTRYPOINT ["python", "/app/services/mcp-server/server.py"]
