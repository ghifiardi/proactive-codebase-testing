# Deployment Playbook

Complete guide for deploying Proactive Codebase Testing Platform to various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Production Checklist](#production-checklist)

---

## Local Development

### Prerequisites

- Python 3.10+
- Virtual environment
- Anthropic API key

### Setup

```bash
# Clone repository
git clone <repo-url>
cd proactive-codebase-testing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Run tests
pytest tests/ -v

# Start development server
uvicorn src.api.server:app --reload
```

---

## Docker Deployment

### Build Image

```bash
# Build for production
docker build -t pct:latest --target api .

# Build for development
docker build -t pct:dev --target development .
```

### Run Container

```bash
# Run API server
docker run -d \
  --name pct-api \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  pct:latest

# Run CLI analysis
docker run --rm \
  -v $(pwd):/workspace \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  pct:latest \
  python -m src.cli.main analyze /workspace --format html --output /workspace/report.html
```

### Docker Compose

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f api
```

---

## Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
# Login: heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-...

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 proactive-codebase-testing

# Create environment
eb create production

# Set environment variables
eb setenv ANTHROPIC_API_KEY=sk-ant-...

# Deploy
eb deploy

# Open
eb open
```

### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/pct

# Deploy
gcloud run deploy pct \
  --image gcr.io/PROJECT_ID/pct \
  --platform managed \
  --region us-central1 \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-... \
  --allow-unauthenticated
```

### Azure Container Instances

```bash
# Build and push
az acr build --registry myregistry --image pct:latest .

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name pct \
  --image myregistry.azurecr.io/pct:latest \
  --environment-variables ANTHROPIC_API_KEY=sk-ant-... \
  --dns-name-label pct-api \
  --ports 8000
```

---

## Kubernetes Deployment

### Create Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pct-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pct-api
  template:
    metadata:
      labels:
        app: pct-api
    spec:
      containers:
      - name: api
        image: your-registry/pct:latest
        ports:
        - containerPort: 8000
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: pct-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### Create Service

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: pct-api
spec:
  selector:
    app: pct-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Deploy

```bash
# Create secret
kubectl create secret generic pct-secrets \
  --from-literal=anthropic-api-key=sk-ant-...

# Apply deployment
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get services
```

---

## Production Checklist

### Pre-Deployment

- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Code coverage >80% (`pytest --cov=src/`)
- [ ] Environment variables configured
- [ ] API keys secured (not in code)
- [ ] Docker image built and tested
- [ ] Health checks configured
- [ ] Logging configured
- [ ] Monitoring setup

### Security

- [ ] API keys stored in secrets manager
- [ ] HTTPS enabled (TLS/SSL)
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation enabled
- [ ] Error messages don't leak sensitive info

### Performance

- [ ] Resource limits set (CPU, memory)
- [ ] Auto-scaling configured
- [ ] Caching enabled (if applicable)
- [ ] Database connection pooling (if applicable)
- [ ] Load testing completed

### Monitoring

- [ ] Health check endpoint working
- [ ] Logging to centralized system
- [ ] Metrics collection enabled
- [ ] Alerting configured
- [ ] Error tracking (Sentry, etc.)

### Backup & Recovery

- [ ] Backup strategy defined
- [ ] Disaster recovery plan
- [ ] Rollback procedure tested
- [ ] Data retention policy

---

## Environment Variables

### Required

- `ANTHROPIC_API_KEY`: Anthropic API key for Claude

### Optional

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `MAX_FILE_SIZE_KB`: Maximum file size to analyze (default: 100)
- `ANALYSIS_TIMEOUT_SECONDS`: Analysis timeout (default: 30)
- `CONFIDENCE_THRESHOLD`: Minimum confidence for findings (default: 0.7)

---

## Troubleshooting

### API not starting

```bash
# Check logs
docker logs pct-api
kubectl logs deployment/pct-api

# Check environment variables
docker exec pct-api env | grep ANTHROPIC
```

### High memory usage

```bash
# Check resource usage
docker stats pct-api
kubectl top pods

# Adjust limits in deployment
```

### Slow responses

```bash
# Check API response times
curl -w "@curl-format.txt" http://localhost:8000/api/health

# Enable debug logging
export LOG_LEVEL=DEBUG
```

---

## Rollback Procedure

### Docker

```bash
# Rollback to previous image
docker stop pct-api
docker rm pct-api
docker run -d --name pct-api -p 8000:8000 pct:previous-version
```

### Kubernetes

```bash
# Rollback deployment
kubectl rollout undo deployment/pct-api

# Check status
kubectl rollout status deployment/pct-api
```

---

## Support

For deployment issues, see:
- [README.md](../README.md)
- [API.md](./API.md)
- GitHub Issues

