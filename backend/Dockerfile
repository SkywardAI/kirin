# Pull gclub/skywardai:0.0.1 base image (Base on Python 3.11.0-slim)
FROM docker.io/gclub/skywardai:0.0.1

# Set the working directory
WORKDIR /app

# Set the server port
EXPOSE 8000

# Copy all files
COPY . .

# Add execution permissions to entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Execute entrypoint.sh for check connection with account_db service
ENTRYPOINT ["/app/entrypoint.sh" ]

# Start up the backend server
CMD uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000
