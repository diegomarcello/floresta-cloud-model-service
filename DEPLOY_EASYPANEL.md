# Deploying to Easypanel

This guide explains how to deploy the **Floresta Cloud Model Service** microservices architecture to [Easypanel.io](https://easypanel.io).

Since this project relies on a **Shared Library** (`shared/`) located at the root, it is critical to configure the **Build Context** correctly for each service.

## Prerequisites

1.  An Easypanel server installed and running.
2.  This repository pushed to a Git provider (GitHub/GitLab) accessible by your Easypanel server.

## Method 1: Docker Compose Import (Recommended)

Easypanel allows you to import services directly from a `docker-compose.yml` file.

1.  Go to your Project in Easypanel.
2.  Click **"Source Control"** (or "Services" -> "From Docker Compose" depending on version).
3.  Connect your repository.
4.  Select the `docker-compose.yml` file path.
5.  **Important**: Easypanel should detect the build contexts defined in the YAML:
    ```yaml
    build:
      context: .
      dockerfile: services/master/Dockerfile
    ```
6.  Review the services list. Ensure Redis and all Python services are listed.
7.  Go to the **Environment** tab for the project (or each service) and add your secrets (from `.env`):
    ```properties
    REDIS_HOST=redis
    REDIS_PORT=6379
    MASTER_POLL_INTERVAL=30
    DATA_COLLECTOR_LIMIT=100
    ML_MODEL_VERSION=v1
    RPA_TIMEOUT=300
    ```
8.  Deploy.

## Method 2: Manual Service Setup

If the import fails or you want granular control, create services manually.

### 1. Redis Service
1.  Click **Create Service** -> **Database** -> **Redis**.
2.  Name: `redis` (Internal hostname will be `redis`).
3.  Port: `6379`.
4.  Create.

### 2. Python Services (Repeat for each service)

For each service (`master`, `ml_inference`, `rpa_worker`, etc.), follow these steps:

1.  **Create Service** -> **App**.
2.  **Source**: Select your Git Repository.
3.  **Build Configuration**:
    *   **Type**: Dockerfile
    *   **Docker Context Directory**: `/` (or `.`) - **CRITICAL**: Must be root to access `shared/`.
    *   **Dockerfile Path**:
        *   Master: `services/master/Dockerfile`
        *   ML Inference: `services/ml_inference/Dockerfile`
        *   RPA Worker: `services/rpa_worker/Dockerfile`
        *   Data Collector: `services/data_collector/Dockerfile`
        *   Data Governance: `services/data_governance/Dockerfile`
        *   LLM Tuner: `services/llm_tuner/Dockerfile`
        *   Monitor: `services/monitor/Dockerfile`
4.  **Environment Variables**:
    *   Add `REDIS_HOST` = `redis` (or the internal IP/host of your Redis service).
    *   Add other variables from `.env`.
5.  **Deploy**.

## Troubleshooting

### "shared module not found"
If the build fails saying it cannot find `shared/` or `floresta_shared`, it means the **Build Context** was not set to the project root.
*   **Fix**: Go to Service Settings -> Build -> Ensure "Context Directory" is set to `/` (Root), NOT `/services/master`.

### Networking
Ensure all services share the same **Private Network** in Easypanel so they can resolve `redis` by hostname.
