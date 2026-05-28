## 🛡️ Fraud AI Triage Platform

An enterprise-grade, multi-service Fraud Detection and Triage Platform built with:

Graph-based fraud detection (GNN)

Gradient Boosted Trees (GBT)

Real-time scoring APIs

Model monitoring & drift detection

Automated triage decision engine

Dockerized microservices architecture

## 📖 Overview

The Fraud AI Triage Platform is a scalable, production-ready fraud detection system designed to:

Detect suspicious financial transactions

Leverage graph relationships between entities

Perform real-time scoring

Automatically triage cases based on risk thresholds

Monitor model drift and performance

Support continuous model retraining

This platform simulates a real-world fintech fraud prevention system.

## 🏗️ Architecture

High-level architecture:

Services Included

Scoring Service – Real-time fraud scoring API

Graph Service – Builds and maintains fraud graph

Training Service – Handles model training pipelines

Triage Agent – Automated risk-based decision logic

Monitoring Layer – Drift detection & metrics

Observability – Prometheus metrics integration

## 🧠 ML Components
1️⃣ Gradient Boosted Trees (GBT)

Tabular transaction features

Risk probability scoring

2️⃣ Graph Neural Network (GNN)

Learns relationships between:

Users

Devices

Accounts

Transactions

Generates embeddings for relational fraud detection

3️⃣ Hybrid Risk Scoring

Combines:

GBT risk score

Graph embedding signals

Velocity features

Historical behavior metrics

## ⚙️ Tech Stack

## ⚙️ Tech Stack

| Layer / Domain            | Tools & Technologies Used |
|---------------------------|---------------------------|
| API Framework             | FastAPI, Uvicorn |
| Machine Learning          | PyTorch (GNN), Scikit-learn (GBT), NumPy, Pandas |
| Graph Processing          | Custom Graph Neural Network Pipeline |
| Feature Engineering       | Custom Feature Store, Velocity Store |
| Model Training Pipelines  | Custom Training Pipelines (GBT, GNN, Calibration) |
| Model Monitoring          | Drift Detection, Performance Metrics Tracking |
| Observability             | Prometheus |
| Data Storage              | Parquet, SQLite (`fraud.db`) |
| Containerization          | Docker, Docker Compose |
| Testing                   | Pytest, Locust (Load Testing) |
| Frontend / Demo UI        | Streamlit |
| Configuration Management  | Pydantic Settings |
| Authentication            | Token-based API Authentication |
| Orchestration / Agents    | Custom Agent Framework (Scoring Agent, Drift Agent, Policy Agent, Graph Agent) |
| Version Control           | Git, GitHub |
---

## 🚀 Running the Project

### 🔹 Option 1: Docker (Recommended)

```bash
docker-compose up --build
```
## 📈 Model Monitoring

The platform includes:

Data drift detection

Model performance tracking

Calibration pipeline

Prometheus metrics endpoint

## 🧪 Testing
Run Unit & Integration Tests
pytest
Load Testing
locust
## 🎯 Key Features

✔ Real-time fraud scoring

✔ Graph-based relationship modeling

✔ Hybrid ML architecture (GBT + GNN)

✔ Microservices design

✔ Drift detection & monitoring

✔ Automated triage decision logic

✔ Production-ready folder structure

✔ Fully Dockerized deployment
