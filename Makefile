FILE_NAME:=.env

# The environment file is used to store all the environment variables for the project.
ENVIRONMENT:=DEV
DEBUG:=True
BACKEND_SERVER_HOST:=127.0.0.1
BACKEND_SERVER_PORT:=8000
BACKEND_SERVER_WORKERS:=4
BACKEND_SERVER_VERSION:=v0.1.16
TIMEZONE:="UTC"

# Database - Postgres
POSTGRES_DB:=my_db
POSTGRES_PASSWORD:=postgres13240!
POSTGRES_PORT:=5432
POSTGRES_SCHEMA:=postgresql
POSTGRES_USERNAME:=postgres
IS_ALLOWED_CREDENTIALS:=True
API_TOKEN:=YOUR-API-TOKEN
AUTH_TOKEN:=YOUR-AUTHENTICATION-TOKEN

# This is the host for Docker Postgres Image in docker-compose.yaml
POSTGRES_HOST:=db

# Database - SQLAlchemy
DB_TIMEOUT:=5
DB_POOL_SIZE:=100
DB_MAX_POOL_CON:=80
DB_POOL_OVERFLOW:=20
IS_DB_ECHO_LOG:=True
IS_DB_EXPIRE_ON_COMMIT:=False
IS_DB_FORCE_ROLLBACK:=True

# JWT Token
JWT_SECRET_KEY:=YOUR-JWT-SECRET-KEY
JWT_SUBJECT:=YOUR-JWT-SUBJECT
JWT_TOKEN_PREFIX:=YOUR-TOKEN-PREFIX
JWT_ALGORITHM:=HS256
JWT_MIN:=60
JWT_HOUR:=23
JWT_DAY:=6

# Hash Functions
HASHING_ALGORITHM_LAYER_1:=bcrypt
HASHING_ALGORITHM_LAYER_2:=argon2
HASHING_SALT:=YOUR-RANDOM-SALTY-SALT

# Codecov (Login to Codecov and get your TOKEN)
# CODECOV_TOKEN:=CODECOV_TOKEN=

# Milvus
ETCD_AUTO_COMPACTION_MODE:=revision
ETCD_AUTO_COMPACTION_RETENTION:=1000
ETCD_QUOTA_BACKEND_BYTES:=4294967296
MILVUS_HOST:=milvus-standalone
MILVUS_PORT:=19530
MILVUS_VERSION:=v2.3.12


DOCKER_VOLUME_DIRECTORY:=

# CPU Accelerate Inference Engine
INFERENCE_ENG:=llamacpp
INFERENCE_ENG_PORT:=8080
INFERENCE_ENG_VERSION:=server--b1-2321a5e
NUM_CPU_CORES:=8.00
NUM_CPU_CORES_EMBEDDING:=4.00

# Embedding engine and it uses same version with Inference Engine
EMBEDDING_ENG:=embedding_eng
EMBEDDING_ENG_PORT:=8080

# Language model, default is phi3-mini-4k-instruct-q4.gguf
# https://github.com/SkywardAI/llama.cpp/blob/9b2f16f8055265c67e074025350736adc1ea0666/tests/test-chat-template.cpp#L91-L92
LANGUAGE_MODEL_NAME:=Phi3-mini-4k-instruct-Q4.gguf
LANGUAGE_MODEL_URL:=https://huggingface.co/aisuko/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi3-mini-4k-instruct-Q4.gguf?download=true
INSTRUCTION:="A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the questions from human."

EMBEDDING_MODEL_NAME:=all-MiniLM-L6-v2-Q4_K_M-v2.gguf
EMBEDDING_MODEL_URL:=https://huggingface.co/aisuko/all-MiniLM-L6-v2-gguf/resolve/main/all-MiniLM-L6-v2-Q4_K_M-v2.gguf?download=true

ADMIN_USERNAME:=admin
ADMIN_EMAIL:=admin@admin.com
ADMIN_PASS:=admin


# yeager
METRICS_PATHS:=runs

.PHONY: env
env:
	@echo "ENVIRONMENT=$(ENVIRONMENT)"> $(FILE_NAME)
	@echo "DEBUG=$(DEBUG)">> $(FILE_NAME)
	@echo "BACKEND_SERVER_HOST=$(BACKEND_SERVER_HOST)">> $(FILE_NAME)
	@echo "BACKEND_SERVER_PORT=$(BACKEND_SERVER_PORT)">> $(FILE_NAME)
	@echo "BACKEND_SERVER_WORKERS=$(BACKEND_SERVER_WORKERS)">> $(FILE_NAME)
	@echo "BACKEND_SERVER_VERSION=$(BACKEND_SERVER_VERSION)">> $(FILE_NAME)
	@echo "POSTGRES_DB=$(POSTGRES_DB)">> $(FILE_NAME)
	@echo "POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)">> $(FILE_NAME)
	@echo "POSTGRES_PORT=$(POSTGRES_PORT)">> $(FILE_NAME)
	@echo "POSTGRES_SCHEMA=$(POSTGRES_SCHEMA)">> $(FILE_NAME)
	@echo "POSTGRES_USERNAME=$(POSTGRES_USERNAME)">> $(FILE_NAME)
	@echo "IS_ALLOWED_CREDENTIALS=$(IS_ALLOWED_CREDENTIALS)">> $(FILE_NAME)
	@echo "API_TOKEN=$(API_TOKEN)">> $(FILE_NAME)
	@echo "AUTH_TOKEN=$(AUTH_TOKEN)">> $(FILE_NAME)
	@echo "POSTGRES_HOST=$(POSTGRES_HOST)">> $(FILE_NAME)
	@echo "DB_TIMEOUT=$(DB_TIMEOUT)">> $(FILE_NAME)
	@echo "DB_POOL_SIZE=$(DB_POOL_SIZE)">> $(FILE_NAME)
	@echo "DB_MAX_POOL_CON=$(DB_MAX_POOL_CON)">> $(FILE_NAME)
	@echo "DB_POOL_OVERFLOW=$(DB_POOL_OVERFLOW)">> $(FILE_NAME)
	@echo "IS_DB_ECHO_LOG=$(IS_DB_ECHO_LOG)">> $(FILE_NAME)
	@echo "IS_DB_EXPIRE_ON_COMMIT=$(IS_DB_EXPIRE_ON_COMMIT)">> $(FILE_NAME)
	@echo "IS_DB_FORCE_ROLLBACK=$(IS_DB_FORCE_ROLLBACK)">> $(FILE_NAME)
	@echo "JWT_SECRET_KEY=$(JWT_SECRET_KEY)">> $(FILE_NAME)
	@echo "JWT_SUBJECT=$(JWT_SUBJECT)">> $(FILE_NAME)
	@echo "JWT_TOKEN_PREFIX=$(JWT_TOKEN_PREFIX)">> $(FILE_NAME)
	@echo "JWT_ALGORITHM=$(JWT_ALGORITHM)">> $(FILE_NAME)
	@echo "JWT_MIN=$(JWT_MIN)">> $(FILE_NAME)
	@echo "JWT_HOUR=$(JWT_HOUR)">> $(FILE_NAME)
	@echo "JWT_DAY=$(JWT_DAY)">> $(FILE_NAME)
	@echo "HASHING_ALGORITHM_LAYER_1=$(HASHING_ALGORITHM_LAYER_1)">> $(FILE_NAME)
	@echo "HASHING_ALGORITHM_LAYER_2=$(HASHING_ALGORITHM_LAYER_2)">> $(FILE_NAME)
	@echo "HASHING_SALT=$(HASHING_SALT)">> $(FILE_NAME)
	@echo "ETCD_AUTO_COMPACTION_MODE=$(ETCD_AUTO_COMPACTION_MODE)">> $(FILE_NAME)
	@echo "ETCD_AUTO_COMPACTION_RETENTION=$(ETCD_AUTO_COMPACTION_RETENTION)">> $(FILE_NAME)
	@echo "ETCD_QUOTA_BACKEND_BYTES=$(ETCD_QUOTA_BACKEND_BYTES)">> $(FILE_NAME)
	@echo "MILVUS_HOST=$(MILVUS_HOST)">> $(FILE_NAME)
	@echo "MILVUS_PORT=$(MILVUS_PORT)">> $(FILE_NAME)
	@echo "MILVUS_VERSION=$(MILVUS_VERSION)">> $(FILE_NAME)
	@echo "DOCKER_VOLUME_DIRECTORY=$(DOCKER_VOLUME_DIRECTORY)">> $(FILE_NAME)
	@echo "METRICS_PATHS=$(METRICS_PATHS)" >> $(FILE_NAME)
	@echo "INFERENCE_ENG=$(INFERENCE_ENG)">> $(FILE_NAME)
	@echo "INFERENCE_ENG_PORT=$(INFERENCE_ENG_PORT)">> $(FILE_NAME)
	@echo "INFERENCE_ENG_VERSION=$(INFERENCE_ENG_VERSION)">> $(FILE_NAME)
	@echo "EMBEDDING_ENG=$(EMBEDDING_ENG)">> $(FILE_NAME)
	@echo "EMBEDDING_ENG_PORT=$(EMBEDDING_ENG_PORT)">> $(FILE_NAME)
	@echo "NUM_CPU_CORES=$(NUM_CPU_CORES)">> $(FILE_NAME)
	@echo "NUM_CPU_CORES_EMBEDDING=$(NUM_CPU_CORES_EMBEDDING)" >> $(FILE_NAME)
	@echo "LANGUAGE_MODEL_NAME=$(LANGUAGE_MODEL_NAME)">> $(FILE_NAME)
	@echo "ADMIN_USERNAME=$(ADMIN_USERNAME)">> $(FILE_NAME)
	@echo "ADMIN_EMAIL=$(ADMIN_EMAIL)">> $(FILE_NAME)
	@echo "ADMIN_PASS=$(ADMIN_PASS)">> $(FILE_NAME)
	@echo "TIMEZONE=$(TIMEZONE)">> $(FILE_NAME)
	@echo "INSTRUCTION"=$(INSTRUCTION)>> $(FILE_NAME)
	@echo "EMBEDDING_MODEL_NAME"=$(EMBEDDING_MODEL_NAME) >> $(FILE_NAME)


.PHONY: prepare
prepare: env
prepare: lm


############################################################################################################
# For development, require Nvidia GPU
.PHONY: build
build: env
	docker compose -f docker-compose.yaml build


.PHONY: up
up: build lm
	docker compose -f docker-compose.yaml up -d


.PHONY: stop
stop:
	docker compose -f docker-compose.yaml stop

.PHONY: logs
logs:
	@docker compose -f docker-compose.yaml logs -f

############################################################################################################
# For demo, without GPU augumentation, but slow for inference. Might include some bugs.
.PHONY: demo
demo: env lm
	docker compose -f docker-compose.demo.yaml up -d

.PHONY: demo-stop
demo-stop:
	docker compose -f docker-compose.demo.yaml stop

.PHONY: demo-logs
demo-logs:
	docker compose -f docker-compose.demo.yaml logs -f

############################################################################################################
# For gpu host.
.PHONY: gpu-up
gpu: env lm
	docker compose -f docker-compose.gpu.yaml up -d

.PHONY: gpu-stop
gpu-stop:
	docker compose -f docker-compose.gpu.yaml stop

.PHONY: gpu-logs
gpu-logs:
	docker compose -f docker-compose.gpu.yaml logs -f

############################################################################################################
# Linter

.PHONY: ruff
ruff:
	@ruff check --output-format=github backend/src/ --config ruff.toml

############################################################################################################
# Download model from Hugging Face

.PHONY: lm
lm:
	@mkdir -p volumes/models && [ -f volumes/models/$(LANGUAGE_MODEL_NAME) ] || wget -O volumes/models/$(LANGUAGE_MODEL_NAME) $(LANGUAGE_MODEL_URL)
	@mkdir -p volumes/models && [ -f volumes/models/$(EMBEDDING_MODEL_NAME) ] || wget -O volumes/models/$(EMBEDDING_MODEL_NAME) $(EMBEDDING_MODEL_URL)


.PHONY: localinfer
localinfer: lm
	@docker run -p 8080:8080 -v ./volumes/models:/models gclub/llama.cpp:$(INFERENCE_ENG_VERSION) -m models/$(LANGUAGE_MODEL_NAME) -c 512 -cnv -i --metrics --host 0.0.0.0 --port 8080

############################################################################################################
# Poetry

.PHONY: poetry
poetry:
	@pipx install poetry==1.8.2

.PHONY: lock
lock:
	@poetry -C backend lock

.PHONY: install
install:
	@poetry -C backend install --no-root -vvv

.PHONY: install-dev
install-dev:
	@poetry -C backend install --only dev --no-root -vvv

.PHONY: plugin
plugin:
	@poetry -C backend self add poetry-plugin-export

.PHONY: expo
expo:
	@poetry -C backend export -f requirements.txt --output backend/requirements.txt

############################################################################################################
# Testing

.PHONY: test
test:
	@pytest backend/tests