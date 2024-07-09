# It should work with this token of anonymous user
curl \
-X 'POST' 'http://0.0.0.0:8000/api/chat' \
-H 'accept: application/json' \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFub255bW91cyIsImVtYWlsIjoiYW5vbnltb3VzQGFub255LmNvbSIsImV4cCI6MTcyMDkxOTY4Nywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.29zUJQvD5dkC9XIRvTfZTFJoO5HzZTgj1JjKOKedg2g' \
-H 'Content-Type: application/json' \
-d '{"sessionUuid": "string", "message": "how are you?"}'