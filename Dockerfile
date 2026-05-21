FROM python:3.14-alpine

ENV HOST=0.0.0.0
ENV PORT=8080
ENV DEBUG=false

WORKDIR /app

# Copy dependency data
COPY src/requirements.txt ./

# Install dependencies
RUN apk add --no-cache curl
RUN pip install -r requirements.txt

# Copy source code
COPY . /app

EXPOSE $PORT

HEALTHCHECK --interval=5s --timeout=3s CMD curl -f http://127.0.0.1:$PORT/api/v1/health || exit 1

CMD ["python", "-u", "/app/app.py"]