# Our base image
FROM gclub/skywardai:v0.1.4

# We set the working directory to /app.
# This is where the application code will be stored.
WORKDIR /app

EXPOSE 8000

COPY . .

# Execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Start up the backend server
CMD ["uvicorn", "src.main:backend_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
