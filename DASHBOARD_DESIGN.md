# DASHBOARD DESIGN

## Analyse des Besoins

Pour concevoir des dashboards efficaces, il faut d'abord analyser :

### Public Cible
- **Équipe SRE**: Métriques techniques, alertes, performance
- **Product Owners**: KPI métier, expérience utilisateur
- **Développeurs**: Performance API, erreurs, debugging
- **Management**: Vue d'ensemble, SLA, disponibilité

### Objectifs du Dashboard
1. **Surveillance en temps réel** - Détection rapide des problèmes
2. **Analyse de tendance** - Capacité planning, optimisation
3. **Post-mortem** - Investigation des incidents
4. **Reporting** - KPI et SLA

## Dashboards Implémentés

### 1. HTTP Overview Dashboard
**Public**: Équipe SRE, Développeurs
**Objectif**: Surveillance temps réel de l'API

**Panels**:
- **Requêtes/seconde** (Time Series) - Volume de trafic
- **Latence P95** (Time Series) - Performance des requêtes
- **Taux d'erreur** (Stat) - Disponibilité
- **Requêtes en cours** (Gauge) - Charge actuelle
- **CPU Usage %** (Time Series) - Ressources système
- **Memory Usage %** (Gauge) - Ressources système

**Justification**: Couvre les métriques essentielles RED (Rate, Errors, Duration) + infrastructure

### 2. Business Metrics Dashboard
**Public**: Product Owners, Management
**Objectif**: KPI métier et utilisation

**Panels**:
- **Prédictions/seconde** (Time Series) - Volume d'activité
- **Application Uptime** (Stat) - Disponibilité
- **Health checks/seconde** (Time Series) - Surveillance
- **Erreurs par type** (Time Series) - Qualité
- **Latence prédictions P95** (Time Series) - Performance métier
- **Distribution âges** (Time Series) - Profil utilisateurs
- **Distribution vitesses** (Time Series) - Contexte trafic

**Justification**: Focus sur les métriques métier et l'expérience utilisateur

## Recommandations de Design

### Hiérarchie Visuelle
1. **En haut**: Métriques critiques (disponibilité, erreurs)
2. **Milieu**: Performance et volume
3. **Bas**: Infrastructure et détails

### Types de Visualisation
- **Time Series**: Tendances temporelles
- **Stat/Gauge**: Valeurs instantanées avec seuils
- **Heatmap**: Distributions (histogrammes)
- **Table**: Comparaisons et détails
- **Pie Chart**: Répartitions (usage modéré)

### Bonnes Pratiques
- **Unités claires**: req/s, %, ms, Go
- **Seuils colorés**: vert/jaune/rouge
- **Légendes explicites**: éviter les abréviations
- **Rafraîchissement adapté**: 5s pour temps réel, 1m pour tendances
- **Temps relatif**: "now-1h to now" par défaut

## Dashboards Supplémentaires Suggérés

### 3. Infrastructure Dashboard
**Métriques node-exporter**:
- CPU par mode (user, system, idle, iowait)
- Mémoire (totale, disponible, cache, swap)
- Disque (espace, I/O read/write, iops)
- Réseau (bandwidth, packets, errors)
- Load average (1min, 5min, 15min)
- File descriptors

### 4. Containers Dashboard
**Métriques cAdvisor**:
- CPU/Mémoire par container
- Réseau par container
- I/O disque par container
- Restarts par container
- Resource limits vs usage

### 5. Database Dashboard
**Métriques PostgreSQL**:
- Connections actives/idles
- Query performance (slow queries)
- Cache hit ratio
- Table sizes et growth
- Lock waits
- Replication lag

### 6. Application Deep Dive
**Métriques détaillées**:
- Distribution latence (P50, P90, P95, P99)
- Erreurs par endpoint
- Heatmap des requêtes par heure
- Top N des requêtes lentes
- Corrélation erreurs/latence

## Variables et Filtres

### Variables Grafana Recommandées
```yaml
# Instance
instance: api-1, api-2, api-3

# Méthode HTTP
method: GET, POST, PUT, DELETE

# Status Code
status: 200, 400, 500

# Time Range
interval: 1m, 5m, 15m, 1h
```

### Utilisation des Variables
- Permettent de filtrer dynamiquement
- Réduisent le nombre de dashboards
- Facilitent l'investigation
- Supportent les comparaisons

## Alerting et Seuils

### Seuils Recommandés
```yaml
# Performance
latency_p95_warning: 500ms
latency_p95_critical: 1000ms

# Disponibilité
error_rate_warning: 5%
error_rate_critical: 10%

# Ressources
cpu_warning: 70%
cpu_critical: 85%
memory_warning: 80%
memory_critical: 90%

# Disque
disk_warning: 80%
disk_critical: 90%
```

### Stratégie d'Alerte
- **Warning**: Investigation requise
- **Critical**: Action immédiate nécessaire
- **Délais**: Éviter les alertes bruyantes
- **Groupement**: Alertes corrélées

## Exemples de Requêtes Avancées

### SLO Calculation
```promql
# Uptime SLA (99.9% = 43.2min downtime/month)
(sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100
```

### Error Budget
```promql
# Error budget remaining
100 - ((sum(rate(http_requests_total{status=~"5.."}[30d])) / sum(rate(http_requests_total[30d]))) * 100)
```

### Capacity Planning
```promql
# CPU trend prediction
predict_linear(cpu_usage[1h], 3600)
```

## Conclusion

Un bon dashboard doit être :
- **Actionnable**: Chaque métrique doit pouvoir déclencher une action
- **Contextuel**: Montrer les relations entre métriques
- **Efficient**: Information maximale, bruit minimal
- **Accessible**: Compréhensible pour le public cible

La clé est d'itérer basé sur l'usage réel et les retours des utilisateurs.
