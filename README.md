# Azure End-to-End Data Pipeline

This repository contains a complete **end-to-end data engineering pipeline** built on Microsoft Azure. It demonstrates how to ingest, transform, store, analyze, and visualize data from an on-premises SQL database to interactive dashboards using the modern Azure stack, following the **Medallion architecture** (Bronze → Silver → Gold).

---

## Project Overview

This project builds a cloud data platform that:

1. Extracts data from an **On-Premises SQL Server** database
2. Orchestrates ingestion with **Azure Data Factory**
3. Stages raw data in **Azure Data Lake Storage Gen2** (Bronze layer)
4. Transforms and cleans data using **Azure Databricks** (PySpark, Serverless Compute, Unity Catalog)
5. Exposes analytics-ready data through **Azure Synapse Analytics** (Serverless SQL Pool)
6. Delivers business insights via **Power BI** dashboards

---

## Architecture Diagram

![Architecture](docs/architecture.png)

**Explanation:**
- Azure Data Factory orchestrates the ingestion pipeline from the on-prem SQL source
- Data flows through the Medallion architecture (Bronze → Silver → Gold) in ADLS Gen2
- Azure Databricks handles all transformation workflows on Serverless compute
- Azure Synapse Analytics serves the Gold layer for analytical queries
- Power BI connects to Synapse to visualize business insights
- Microsoft Entra ID and Key Vault secure access across the platform

---

## Pipeline Flow

1. **Ingestion (Azure Data Factory)**
   A parameterized pipeline (`Lookup` + `ForEach`) copies tables from the on-prem SQL Server into the *Bronze* layer of ADLS Gen2.

2. **Transformation (Azure Databricks)**
   A Databricks Job reads the Bronze data, normalizes date formats, and writes clean data to the *Silver* layer. A second Job harmonizes column names (snake_case) and writes the final *Gold* tables in Delta format.

3. **Analytics (Azure Synapse)**
   SQL views are dynamically created over the Gold layer using `OPENROWSET` with `FORMAT = 'DELTA'`, exposing analytics-ready data through Synapse Serverless SQL.

4. **Visualization (Power BI)**
   Power BI connects directly to the Synapse Serverless SQL endpoint to build interactive dashboards.

### ADF Pipeline

![ADF Pipeline](docs/adf_pipeline.png)

This pipeline uses:
- A `Lookup` activity to retrieve the list of tables to copy
- A `ForEach` loop with a `Copy Data` activity for ingestion
- Two Databricks **Job** activities (Serverless-compatible) for the Bronze→Silver and Silver→Gold transformations

---

## Tech Stack

- **Azure Data Factory** – orchestrates ingestion and scheduling
- **Azure Data Lake Storage Gen2** – stores raw and processed datasets
- **Azure Databricks** – scalable Spark transformations (Serverless Compute, Unity Catalog)
- **Delta Lake** – storage format for the Silver and Gold layers
- **Azure Synapse Analytics** – Serverless SQL pool for analytics
- **Microsoft Entra ID & Azure Key Vault** – secure credentials and access governance
- **Power BI** – interactive dashboards
- **SQL Server** – on-premises source system

---

## Dataset

This project uses the official Microsoft sample database:

- **AdventureWorksLT** (Sample OLTP database)
  https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure

AdventureWorksLT is a lightweight transactional sample database provided by Microsoft that simulates a manufacturing/retail company scenario.

---

## Project Structure

```
azure-end-to-end-data-pipeline/
├── README.md
├── notebooks/
│   ├── bronze_to_silver.py
│   └── silver_to_gold.py
├── adf/
│   └── copy_all_tables_pipeline.json
├── synapse/
│   └── create_gold_views.sql
├── docs/
│   ├── architecture.png
│   └── adf_pipeline.png
└── .gitignore
```

---

## Setup Instructions

### Prerequisites

- Azure Subscription
- Power BI Desktop
- Access to a SQL Server instance (on-prem or Azure SQL)

### Deployment Steps

1. Provision Azure services: ADLS Gen2, Data Factory, Databricks, Synapse, Key Vault
2. Configure the ADF pipeline for ingestion (`adf/copy_all_tables_pipeline.json`)
3. Deploy the Databricks notebooks as Serverless Jobs (`notebooks/`)
4. Run `synapse/create_gold_views.sql` to expose the Gold layer as SQL views
5. Connect Power BI to the Synapse Serverless SQL endpoint and build reports

---

## Key Features

- Medallion architecture for structured, incremental data refinement
- Fully automated pipeline with parameterized ADF activities and a daily schedule trigger
- Serverless compute throughout (Databricks + Synapse) — no cluster management, pay-per-use
- Governed data access via Unity Catalog External Locations and Managed Identity Storage Credentials
- Delta Lake tables written with cross-tool compatibility in mind (Synapse Serverless SQL support)

---

## Technical Challenges Solved

- **Azure compute quotas** — migrated from classic clusters to **Serverless compute** to avoid regional VM quota limitations on a free-tier subscription.
- **Access governance** — replaced legacy DBFS mounts (incompatible with Serverless) with **Unity Catalog External Locations** backed by a Storage Credential tied to an Access Connector (Managed Identity).
- **Cross-tool Delta compatibility** — disabled **Deletion Vectors** at write time so that Gold tables written by Databricks (protocol v3/v7 by default) remain readable by Synapse Serverless SQL (which only supports protocol v1/v2).
- **ADF/Databricks orchestration** — replaced classic "Notebook" activities with Databricks **Job** activities, the only activity type compatible with Serverless compute in Azure Data Factory pipelines.

---

## Future Enhancements

- Real-time streaming ingestion (Event Hub / Kafka)
- CI/CD with Azure DevOps or GitHub Actions
- Automated data quality testing and monitoring
- ML integration for predictive analytics

---

## Author

**Bilal Khallabi**
Data Engineering / Data Science — Master Big Data & Intelligent Systems

[LinkedIn](https://linkedin.com/in/bilal-khallabi-0a1a8a315) · [GitHub](https://github.com/Bilal51002)
