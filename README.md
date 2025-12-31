# Floresta Cloud Model Service

A comprehensive service mesh for Intelligent Automation, ML, and Data Governance.

## Architecture

- **Pattern**: Microservices with Central Orchestration.
- **Communication**: Asynchronous Messaging via Redis (Pub/Sub & Queues).
- **Deployment**: Docker Containers managed by Docker Compose.

## Services

1.  **Master**: The orchestrator that dispatches tasks and manages lifecycles.
2.  **Data Collector**: Gathers data from configured sources.
3.  **Data Governance**: Validates data against schemas and policies.
4.  **ML Inference**: Hosting standard ML models.
5.  **LLM Tuner**: Specialized service for LLM fine-tuning and heavy inference.
6.  **RPA Worker**: Executes robotic process automation scripts.
7.  **Monitor**: Health checks and system metrics.

## Development

All services share the `shared/` library. 
To start the stack:

```bash
docker-compose up --build
```
