FROM gclub/skywardai:v0.1.2

WORKDIR /app

EXPOSE 8000

COPY . .

# Execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Start up the backend server
CMD uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000
