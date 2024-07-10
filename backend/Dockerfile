# Our base image
FROM python:3.11.8-slim

# We set the working directory to /app.
# This is where the application code will be stored.
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# netcat for nc command
# If necessary gcc postgresql
RUN apt-get update \
  && apt-get -y install netcat-traditional curl \
  && apt-get clean

COPY . .

RUN pip --disable-pip-version-check --no-cache-dir install -r requirements.txt && rm -rf /tmp/pip-tmp

EXPOSE 8000

HEALTHCHECK --interval=60s --timeout=30s --retries=5 CMD ["curl", "-f", "http://localhost:8000/api/health"]

# Execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Start up the backend server
CMD ["uvicorn", "src.main:backend_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
