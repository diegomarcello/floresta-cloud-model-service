# Makefile for Floresta Cloud Model Service

# Load .env file if it exists
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Default target
all: help

help:
	@echo "Available commands:"
	@echo "  make up               - Start all services with Docker Compose"
	@echo "  make down             - Stop all services"
	@echo "  make build            - Build all services"
	@echo "  make logs             - Tail logs for all services"
	@echo ""
	@echo "  make master           - Build and start only the Master service"
	@echo "  make ml               - Build and start only the ML Inference service"
	@echo "  make rpa              - Build and start only the RPA Worker service"
	@echo "  make collector        - Build and start only the Data Collector service"
	@echo "  make governance       - Build and start only the Data Governance service"
	@echo "  make llm              - Build and start only the LLM Tuner service"
	@echo "  make monitor          - Build and start only the Monitor service"
	@echo "  make redis            - Start Redis only"

# ----------------------------------------------------------------------
# Full Stack Management
# ----------------------------------------------------------------------

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

# ----------------------------------------------------------------------
# Individual Service Management
# ----------------------------------------------------------------------

redis:
	docker-compose up -d redis

master:
	docker-compose up -d --build master

ml:
	docker-compose up -d --build ml_inference

rpa:
	docker-compose up -d --build rpa_worker

collector:
	docker-compose up -d --build data_collector

governance:
	docker-compose up -d --build data_governance

llm:
	docker-compose up -d --build llm_tuner

monitor:
	docker-compose up -d --build monitor

# ----------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------

clean:
	docker-compose down -v --remove-orphans
