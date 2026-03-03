FROM python:3.11-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir locust

COPY locustfile.py .

EXPOSE 8089

CMD ["locust", "-f", "locustfile.py", "--host", "http://api:8000"]
