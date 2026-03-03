# VEILLE OBSERVABILITÉ

## Questions de Recherche

### 1. Différence Monitoring vs Observabilité
**Monitoring**: Surveillance passive basée sur des métriques prédéfinies pour détecter des problèmes connus.
**Observabilité**: Capacité à comprendre l'état interne d'un système à partir de ses données externes (métriques, logs, traces).

### 2. Les 3 Piliers de l'Observabilité
1. **Métriques** - Données numériques temporelles (CPU, mémoire, requêtes/sec)
2. **Logs** - Événements textuels avec timestamps et contexte
3. **Traces** - Suivi des requêtes à travers les services distribués

### 3. Architecture Pull de Prometheus
- Prometheus scrape (tire) les métriques des endpoints `/metrics`
- Les applications exposent leurs métriques via HTTP
- Avantages: simplicité, pas de push complexe, contrôle centralisé
- Inconvénients: découverte de services, réseau privé

### 4. Types de Métriques Prometheus
- **Counter**: Monotonique, ne fait qu'augmenter (ex: requêtes totales)
- **Gauge**: Valeur instantanée qui peut monter/descendre (ex: CPU, mémoire)
- **Histogram**: Distribution des valeurs avec buckets (ex: latences)
- **Summary**: Similar à histogram avec quantiles calculés côté client

### 5. Bonnes Pratiques de Nommage
- Utiliser des noms descriptifs en snake_case
- Préfixer par le nom de l'application: `app_`
- Inclure l'unité dans le nom: `_seconds`, `_bytes`, `_total`
- Utiliser des labels pour la segmentation: `app_requests_total{method="GET", status="200"}`

### 6. PromQL Essentiel
- `rate(metric[5m])` - Taux de changement sur 5 minutes
- `increase(metric[5m])` - Augmentation absolue sur 5 minutes
- `histogram_quantile(0.95, rate(metric_bucket[5m]))` - 95ème percentile
- `sum by (label) (metric)` - Agrégation par label
- `topk(10, metric)` - Top 10 des valeurs

### 7. Méthodologie RED
- **Rate**: Taux de requêtes par seconde
- **Errors**: Taux d'erreurs par rapport au total
- **Duration**: Latence des requêtes (P50, P95, P99)

### 8. Méthodologie USE
- **Utilization**: Pourcentage de ressource utilisée
- **Saturation**: Charge actuelle vs capacité
- **Errors**: Taux d'erreurs de la ressource

## Réponses Détaillées

### Q1: Pourquoi utiliser des buckets dans les histogrammes?
Les buckets permettent de stocker efficacement des distributions sans garder chaque valeur individuelle. Ils permettent de calculer des quantiles (P95, P99) et sont plus performants que de stocker chaque mesure.

### Q2: Comment choisir les seuils d'alerte?
- Basés sur les SLO/SLA métier
- Utiliser les percentiles historiques (P95 + 2σ)
- Éviter les alertes bruyantes avec des fenêtres temporelles
- Implémenter des alertes multi-niveaux (warning, critical)

### Q3: Quelle différence entre cAdvisor et node-exporter?
- **node-exporter**: Métriques système hôte (CPU, RAM, disque, réseau)
- **cAdvisor**: Métriques par container Docker (ressources limites/usage)
- Complémentaires: node-exporter pour l'hôte, cAdvisor pour les conteneurs

### Q4: Optimiser les performances de Prometheus?
- Configurer la rétention appropriée
- Utiliser le recording rules pour les requêtes complexes
- Optimiser les labels (cardinalité modérée)
- Monitorer la performance de Prometheus lui-même

### Q5: Sécurité du monitoring en production?
- Ne pas exposer Prometheus directement sur internet
- Utiliser reverse proxy avec authentification
- Chiffrer les communications (HTTPS/TLS)
- Limiter l'accès aux métriques sensibles
- Isoler le réseau de monitoring
