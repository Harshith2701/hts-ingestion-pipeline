# 🧾 HTS Ingestion Pipeline

Hey! This is a personal project I built to learn how to set up a data pipeline using Docker, Airflow, and Postgres — and eventually explore and visualize some U.S. trade data in Power BI.

## 🗃️ What’s the data?

The data comes from the **U.S. International Trade Commission** — specifically the **Harmonized Tariff Schedule (HTS)** in JSON format.

Each entry is a tariff classification line. It includes:
- A unique code (`htsno`)
- A description of the product
- Its indentation level (how deeply nested the item is)
- General and special duty rates
- Some entries are just labeled "Other" — which I mark with a flag for filtering later

Basically, it’s a giant list of how different goods are classified and taxed when imported.

---

## 🧠 Why I chose this dataset

It’s weirdly interesting. It shows how governments categorize literally everything from live horses to semiconductors.

Plus:
- It’s structured, but still needs cleaning
- It has real-world use (trade, tariffs, policy)
- I wanted to try processing something bigger and a bit messy

---

## 🔧 What I built

This project does 3 main things:

1. **Ingests HTS JSON data from a public URL**
2. **Cleans it up and loads it into Postgres**
3. **Automates the whole thing using Airflow**

After that, I pulled the cleaned data into Power BI to explore it visually.

---

## 🛠️ Tech stack

- **Python** for parsing and ingesting the data
- **Airflow** to automate the task on a schedule
- **PostgreSQL** to store the cleaned data
- **Docker** to containerize everything
- **Power BI** for dashboards

---

## 📦 How the pipeline works

1. **Docker Compose** spins up:
   - A Postgres database
   - An Airflow container
   - An app container that runs the ingestion script

2. **Airflow DAG** triggers every 10 minutes (just for testing, can be changed)
3. It runs the Python function that:
   - Streams the large JSON
   - Cleans up text fields
   - Flags "other" items
   - Inserts it into the `hts_data` table in Postgres
4. I then use Power BI to connect to the DB and create visuals

---

## 📊 What I visualized in Power BI

- Count of HTS codes at each indent level (shows how detailed classification gets)
- Share of "Other" entries (which are vague catch-all lines)
- Most common general and special duty rates
- A searchable table of all items

It helped me spot which sections are bloated with vague "other" items, and where tariff rates cluster.

---

## 🧹 Cleaning choices I made

I dropped:
- `units`, `other`, and `footnotes` — they weren’t adding much value
- Cleaned up extra whitespace
- Flagged entries that just said "Other" in the description

---

## 📁 File overview

- `docker-compose.yml` – brings everything up
- `my_ingest.py` – core logic to stream + clean + insert
- `ingest_chunks.py` – Airflow DAG that runs the job
- `Dockerfile` – for the app container
- `requirements.txt` – Python dependencies

---

## 💭 Final thoughts

This wasn’t about building something perfect — I just wanted to get hands-on with Airflow, work with real JSON data, and hook it into Power BI. And now I know how to do that. Pretty cool.

---

