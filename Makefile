# Makefile
include makefile_docker_compose.mk

.PHONY: format f

# Override up to create directories with proper permissions
up:
	mkdir -p .docker_volumes/prometheus/data
	chmod 777 .docker_volumes/prometheus/data
	mkdir -p .docker_volumes/grafana/data
	chmod 777 .docker_volumes/grafana/data
	mkdir -p .docker_volumes/loki/data/{index,cache,chunks}
	chmod 777 .docker_volumes/loki/data
	mkdir -p .docker_volumes/loki/wal
	chmod 777 .docker_volumes/loki/wal
	mkdir -p .docker_volumes/loki/compactor
	chmod 777 .docker_volumes/loki/compactor
	$(DC_BIN) up -d

format:
	prettier --write .

f: format
