# 🌊 AqNet

**AqNet** is the data pipeline (ETL) for building an **aquarium knowledge graph**.  
It ingests relational data (starting with [FishBase](https://www.fishbase.se/)) and loads it into [Neo4j](https://neo4j.com/) as a property graph, enabling queries about species, taxonomy, ecology, and compatibility.

---

## 📐 Overview

The pipeline follows a simple **ETL** pattern:

1. **Extract**  
   - Download/export FishBase (MySQL dump → CSVs).

2. **Transform**  
   - Map relational tables into nodes (Species, Families, Orders, etc).  
   - Define relationships from foreign keys (e.g., *Species → Family*, *Predator → Prey*).  

3. **Load**  
   - Push nodes and edges into Neo4j with indexes for fast querying.  

---

## 🛠 Tech Stack
- **Python** (ETL orchestration)
- **Neo4j** (graph database)
- **Cypher** (queries)
- **YAML configs** (mapping tables → nodes/edges)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Neo4j (desktop or server)
- MySQL (for original FishBase dump)

### Setup
```bash
git clone https://github.com/joelhutchinson/aqnet.git
cd aqnet
pip install -r requirements.txt
