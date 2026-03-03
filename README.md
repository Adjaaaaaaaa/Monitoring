# Monitoring & Observabilité : FastAPI + Prometheus + Grafana

Stack complète de monitoring et d'observabilité pour application FastAPI avec Prometheus, Grafana, Locust et Docker.

##  Objectif

Implémenter une solution de monitoring production-ready pour une API FastAPI de prédiction d'accidents, incluant :
- **Instrumentation** des métriques Prometheus
- **Visualisation** Grafana 
- **Test de charge** Locust
- Alerting automatique

##  Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FastAPI    │    │  Prometheus  │    │   Grafana    │
│   :8000      │───▶│   :9090      │───▶│   :3000      │
│   /metrics   │    │   Scrape     │    │   Dashboards │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL   │    │node-exporter│    │   Locust     │
│   :5432      │    │   :9100      │    │   :8089      │
│   Database   │    │  System     │    │  Load Test   │
└─────────────┘    └─────────────┘    └─────────────┘
```

##  Quick Start

### Prérequis
- Docker & Docker Compose
- Git

### Démarrage
```bash
# Cloner le projet
git clone https://github.com/Adjaaaaaaaa/Monitoring.git
cd Monitoring

# Démarrer la stack complète
docker-compose -f docker-compose.monitoring.yml up -d

# Vérifier les services
docker-compose -f docker-compose.monitoring.yml ps
```

### Accès aux services
- **API FastAPI** : http://localhost:8000
- **Grafana** : http://localhost:3000 (admin/admin)
- **Prometheus** : http://localhost:9090
- **Locust** : http://localhost:8089
- **cAdvisor** : http://localhost:8080

##  Métriques Implémentées

### Business Metrics
- `predictions_total` : Nombre total de prédictions
- `health_checks_total` : Health checks effectués
- `app_uptime_seconds` : Uptime de l'application
- `prediction_confidence_histogram` : Distribution confiance prédictions
- `age_histogram` : Distribution âges utilisateurs
- `speed_histogram` : Distribution vitesses

### HTTP Metrics
- `http_requests_total` : Requêtes HTTP par handler/méthode/status
- `http_request_duration_seconds` : Latence des requêtes
- `http_errors_total` : Erreurs HTTP par type

### Infrastructure Metrics
- CPU, Memory, Disk (node-exporter)
- Container metrics (cAdvisor)

##  Dashboards Grafana

### Dashboards Simples (recommandés pour commencer)
- **Simple Business Dashboard** : Vue claire des métriques métier
- **Simple HTTP Dashboard** : Infrastructure essentielle

### Dashboards Complets (avancés)
- **Business Metrics Dashboard** : Métriques détaillées avec latence P95
- **HTTP Overview Dashboard** : Vue complète avec erreurs

##  Stress Testing avec Locust

### Configuration
- **Accès** : http://localhost:8089
- **Profils utilisateurs** : AccidentPredictionUser, ReadOnlyUser, StressTestUser
- **Host cible** : http://api:8000

### Scénarios de test
```bash
# Test léger (10 utilisateurs)
Number of users: 10
Spawn rate: 2

# Test modéré (50 utilisateurs)
Number of users: 50
Spawn rate: 5

# Test intense (200+ utilisateurs)
Number of users: 200
Spawn rate: 10
```

##  Alerting

### Règles configurées
- **HighErrorRate** : > 10% d'erreurs HTTP
- **HighLatency** : P95 > 1s
- **HighCPUUsage** : > 80% CPU
- **HighMemoryUsage** : > 85% RAM
- **LowDiskSpace** : < 10% disque disponible

##  Structure du Projet

```
Monitoring/
├── api/app/
│   ├── metrics.py          # Instrumentation Prometheus
│   ├── main.py            # Configuration FastAPI
│   └── routes.py          # Endpoints instrumentés
├── monitoring/
│   ├── grafana/
│   │   ├── provisioning/  # Configuration datasource/dashboards
│   │   └── dashboards/    # Dashboards JSON (4 fichiers)
│   ├── prometheus/
│   │   ├── prometheus.yml # Configuration scraping
│   │   └── rules/         # Règles d'alerting
│   └── locust/
│       ├── locustfile.py  # Scénarios de test
│       └── Dockerfile     # Container Locust
├── docker-compose.monitoring.yml
├── MONITORING_GUIDE.md    # Guide complet
├── DASHBOARD_DESIGN.md    # Conception dashboards
└── VEILLE_OBSERVABILITE.md # Recherche & concepts
```

##  Requêtes PromQL Utiles

### Business Metrics
```promql
# Prédictions par seconde
rate(predictions_total{success="True"}[5m])

# Total prédictions
predictions_total{success="True"}

# Uptime application
app_uptime_seconds
```

### HTTP Metrics
```promql
# Requêtes par seconde
rate(http_requests_total[5m])

# Taux d'erreur
rate(http_requests_total{status!~"2.."}[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Infrastructure
```promql
# CPU Usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

##  Commandes Utiles

```bash
# Démarrer/arrêter la stack
docker-compose -f docker-compose.monitoring.yml up -d
docker-compose -f docker-compose.monitoring.yml down

# Logs des services
docker-compose -f docker-compose.monitoring.yml logs api
docker-compose -f docker-compose.monitoring.yml logs grafana
docker-compose -f docker-compose.monitoring.yml logs prometheus

# Vérifier les métriques
curl http://localhost:8000/metrics

# Redémarrer Grafana (après modification dashboards)
docker-compose -f docker-compose.monitoring.yml restart grafana
```

##  Documentation

- **[MONITORING_GUIDE.md](MONITORING_GUIDE.md)** : Guide complet d'utilisation
- **[DASHBOARD_DESIGN.md](DASHBOARD_DESIGN.md)** : Principes de conception des dashboards
- **[VEILLE_OBSERVABILITE.md](VEILLE_OBSERVABILITE.md)** : Recherche et concepts

