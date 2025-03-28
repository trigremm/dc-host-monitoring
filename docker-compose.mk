# docker-compose.mk
all: ps

ps:
	docker compose ps

logs:
	while true; do docker compose logs -f --tail 100; sleep 10 ;done

prune:
	docker system prune -f -a

pull:
	git pull

build:
	docker compose build

up:
	# prepare directories with proper permissions
	mkdir -p .docker_volumes/prometheus/data
	chmod 777 .docker_volumes/prometheus/data
	mkdir -p .docker_volumes/grafana/data
	chmod 777 .docker_volumes/grafana/data
	mkdir -p .docker_volumes/grafana/dashboards
	chmod -R 755 .docker_volumes/grafana/dashboards
	mkdir -p .docker_volumes/grafana/provisioning
	chmod -R 755 .docker_volumes/grafana/provisioning
	mkdir -p .docker_volumes/loki/data/{index,cache,chunks}
	chmod 777 .docker_volumes/loki/data
	mkdir -p .docker_volumes/loki/wal
	chmod 777 .docker_volumes/loki/wal
	mkdir -p .docker_volumes/loki/compactor
	chmod 777 .docker_volumes/loki/compactor
	# start services
	docker compose up -d --no-build

stop:
	docker compose stop

down:
	docker compose down

restart: stop up

recreate: pull build stop up ps

r: recreate

rl: recreate logs