# makefile_docker_compose.mk
DC_BIN := docker compose

.PHONY: d r l rl
.PHONY: deploy recreate
.PHONY: ps logs build up stop down

# aliases
d: deploy
r: recreate
l: logs
rl: r l

# main
deploy:
	git pull
	$(MAKE) recreate

recreate: build stop up

# docker compose
ps:
	$(DC_BIN) ps

logs:
	$(DC_BIN) logs -f -n 100

build:
	$(DC_BIN) build

up:
	$(DC_BIN) up -d

stop:
	$(DC_BIN) stop

down:
	$(DC_BIN) down --remove-orphans
