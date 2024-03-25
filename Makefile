.PHONY: env
env:
	@cp .env.example .env

############################################################################################################
# For development, require Nvidia GPU
.PHONY: build
build: env
	docker-compose -f docker-compose.yaml build


.PHONY: up
up: env build
	docker-compose -f docker-compose.yaml up -d


.PHONY: stop
stop:
	docker-compose -f docker-compose.yaml stop

############################################################################################################
# For demo, without GPU augumentation, but slow for inference. Might include some bugs.
.PHONY: demo
demo: env
	docker-compose -f docker-compose.demo.yaml build
	docker-compose -f docker-compose.demo.yaml up -d

.PHONY: demo-stop
demo-stop:
	docker-compose -f docker-compose.demo.yaml stop

.PHONY: demo-logs
demo-logs:
	docker-compose -f docker-compose.demo.yaml logs -f

.PHONY: demo-remove
demo-remove:
	docker-compose -f docker-compose.demo.yaml down
