# Monitoring & Observabilité Setup

## Architecture Complète

Ce projet implémente une stack de monitoring complète pour l'API FastAPI de prédiction d'accidents avec :

### Services Principaux
- **FastAPI** (port 8000) - API avec métriques intégrées
- **PostgreSQL** (port 5432) - Base de données
- **Streamlit** (port 8501) - Interface utilisateur

### Stack de Monitoring
- **Prometheus** (port 9090) - Collecte et stockage des métriques
- **Grafana** (port 3000) - Visualisation et dashboards
- **Node Exporter** (port 9100) - Métriques système hôte
- **cAdvisor** (port 8080) - Métriques containers Docker
- **Locust** (port 8089) - Tests de charge

## Démarrage Rapide

### 1. Lancer la stack complète
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

### 2. Accéder aux services
- **API FastAPI**: http://localhost:8000
- **Métriques API**: http://localhost:8000/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Locust**: http://localhost:8089
- **Node Exporter**: http://localhost:9100/metrics
- **cAdvisor**: http://localhost:8080

## Métriques Implémentées

### Métriques Applicatives
- `predictions_total` - Nombre total de prédictions (avec labels version/succès)
- `health_checks_total` - Nombre total de health checks
- `http_errors_total` - Erreurs HTTP segmentées par type et code
- `app_uptime_seconds` - Temps de fonctionnement de l'application
- `active_connections` - Nombre de connexions actives

### Histogrammes Business
- `prediction_confidence_histogram` - Distribution des confiances de prédiction
- `age_histogram` - Distribution des âges des utilisateurs
- `speed_histogram` - Distribution des vitesses limites
- `model_prediction_duration_seconds` - Latence des prédictions

### Métriques Infrastructure
- **CPU**: Utilisation par mode (user, system, idle, iowait)
- **Mémoire**: Totale, disponible, cache, swap
- **Disque**: Espace utilisé, I/O read/write
- **Réseau**: Octets entrants/sortants, paquets, erreurs
- **Load Average**: Charge système 1min, 5min, 15min

## Dashboards Grafana

### 1. HTTP Overview Dashboard
- Requêtes/seconde par méthode et status
- Latence P95
- Taux d'erreur avec seuils colorés
- Requêtes en cours
- Utilisation CPU et mémoire

### 2. Business Metrics Dashboard
- Prédictions par seconde
- Uptime de l'application
- Distribution des âges et vitesses
- Erreurs par type
- Latence des prédictions

## Tests de Charge avec Locust

### Profils Utilisateurs
1. **AccidentPredictionUser** - Usage normal (70% prédictions, 30% health checks)
2. **ReadOnlyUser** - Lecture seule (health checks uniquement)
3. **StressTestUser** - Test de charge intensive

### Scénarios de Test
```bash
# Test léger - 20 utilisateurs
curl -X POST http://localhost:8089/swarm \
  -H "Content-Type: application/json" \
  -d '{"locust_count": 20, "hatch_rate": 5, "user_class": "AccidentPredictionUser"}'

# Test moyen - 100 utilisateurs
curl -X POST http://localhost:8089/swarm \
  -H "Content-Type: application/json" \
  -d '{"locust_count": 100, "hatch_rate": 10, "user_class": "AccidentPredictionUser"}'

# Test intensif - 200 utilisateurs
curl -X POST http://localhost:8089/swarm \
  -H "Content-Type: application/json" \
  -d '{"locust_count": 200, "hatch_rate": 20, "user_class": "StressTestUser"}'
```

## Requêtes PromQL Essentielles

### Métriques HTTP
```promql
# Requêtes par seconde
rate(http_requests_total[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Taux d'erreur
(rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) * 100
```

### Métriques Business
```promql
# Prédictions par seconde
rate(predictions_total[5m])

# Distribution des âges
histogram_quantile(0.50, rate(age_histogram_bucket[5m]))

# Erreurs par type
rate(http_errors_total[5m])
```

### Infrastructure
```promql
# CPU Usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk Usage
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100
```

## Alerting

### Règles Configurées
- **HighErrorRate** > 10% d'erreurs
- **HighLatency** P95 > 1s
- **HighCPUUsage** > 80%
- **HighMemoryUsage** > 85%
- **LowDiskSpace** < 10% disponible
- **ApplicationDown** API inaccessible

## Points d'Accès API

### Endpoints Principaux
- `GET /health` - Health check
- `POST /predict` - Prédiction d'accident
- `GET /metrics` - Métriques Prometheus

### Endpoints de Test
- `GET /metrics-test` - Génère des métriques de test
- `GET /error-test?error_type=validation` - Génère des erreurs de test

## Bonnes Pratiques

### Monitoring
- Surveiller les 3 piliers : métriques, logs, traces
- Utiliser la méthodologie RED (Rate, Errors, Duration)
- Définir des SLO/SLA réalistes
- Mettre en place des alertes pertinentes

### Performance
- Identifier les goulots d'étranglement avec les tests de charge
- Optimiser les requêtes lentes
- Surveiller l'utilisation des ressources
- Planifier le scaling horizontal/vertical

### Sécurité
- Ne pas exposer Prometheus en production
- Sécuriser l'accès à Grafana
- Limiter l'accès aux métriques sensibles
- Utiliser HTTPS pour tous les services

## Dépannage

### Problèmes Communs
1. **Prometheus ne scrape pas** - Vérifier les targets dans l'interface Prometheus
2. **Grafana ne montre pas de données** - Vérifier la datasource Prometheus
3. **Métriques manquantes** - Redémarrer l'API avec `ENABLE_METRICS=true`
4. **Locust ne se connecte pas** - Vérifier le réseau Docker

### Logs Utiles
```bash
# Logs de tous les services
docker-compose -f docker-compose.monitoring.yml logs -f

# Logs d'un service spécifique
docker-compose -f docker-compose.monitoring.yml logs -f api
docker-compose -f docker-compose.monitoring.yml logs -f prometheus
docker-compose -f docker-compose.monitoring.yml logs -f grafana
```

## Extensions Possibles

1. **AlertManager** - Notifications avancées
2. **Jaeger** - Distributed tracing
3. **ELK Stack** - Centralisation des logs
4. **Thanos** - Stockage distribué Prometheus
5. **Kubernetes** - Orchestration conteneurs
