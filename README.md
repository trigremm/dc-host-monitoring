# dc-host-monitoring

Host monitoring stack: Prometheus + Grafana + Loki + Promtail + Node Exporter + cAdvisor + Alertmanager.

## Quick start

```bash
cp .env.sample .env
vim .env
make up
```

> **Note:** `make up` creates volume directories with proper permissions (grafana uid 472, prometheus nobody).

## Commands

### Lifecycle

```
make d          # deploy (git pull + recreate)
make r          # recreate (build + stop + up)
make up         # start (creates volumes with permissions)
make stop       # stop
make down       # stop and remove
make ps         # status
make l          # follow logs
```

### Formatting

```
make format     # prettier --write .
make f          # alias for format
```

## Web UIs

- Grafana: http://localhost:3000 (default: admin/admin)
- Prometheus: http://localhost:9090

## Setup Grafana

1. Open Grafana at http://localhost:3000
2. Add data source: Prometheus → `http://prometheus:9090`
3. Import dashboards: 1860, 20825, 11277
