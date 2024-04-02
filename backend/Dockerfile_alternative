FROM gclub/skywardai:v0.1.2

WORKDIR /app

EXPOSE 8000

# Install Python dependencies
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# Execute entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# Start up the backend server
CMD uvicorn src.main:backend_app --workers 1 --host 0.0.0.0 --port 8000
