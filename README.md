# dc-host-monitoring

Host monitoring stack: Prometheus + Grafana + Loki + Promtail + Node Exporter + cAdvisor + Alertmanager.

## Quick start

```bash
cp .env.sample .env
vim .env
make up
```

> **Note:** `make up` pre-creates the `.docker_volumes/` data directories (prometheus, grafana, loki) with `chmod 777` so each container's own user can write to them.

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
- Loki API: http://localhost:3100 (no UI of its own — query logs via Grafana → Explore)

## Grafana provisioning

Datasources (Prometheus, Loki) and the three dashboards (node-exporter full, docker/cAdvisor, Loki logs) are provisioned automatically from `grafana/provisioning/` and `grafana/dashboards/` on start — nothing to add or import by hand. To change a dashboard, edit its JSON there and restart Grafana.
