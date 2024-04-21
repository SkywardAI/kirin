# Our base image
FROM gclub/skywardai:v0.1.8

# We set the working directory to /app.
# This is where the application code will be stored.
WORKDIR /app

EXPOSE 8000

COPY . .
RUN pip install kimchima==0.4.8 \
&& pip install -U huggingface_hub hf_transfer \
&& export HF_HUB_HF_ENABLE_TRANSFER=1 \
&& export HF_ENDPOINT=https://hf-mirror.com
# Execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Start up the backend server
CMD ["uvicorn", "src.main:backend_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
