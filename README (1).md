
# Mamaearth Data Analysis Pipeline

## 1. SQL Setup and Reports

The SQL pipeline is used to create the database schema, load the seed data, and run the reporting queries.

Run the SQL files in this order:

1. `sql/schema.sql`
2. `sql/seed_data.sql`
3. `sql/reports.sql`

The schema should be created first, followed by loading the supplied seed data. The reporting SQL is then run against the populated database.

---

## 2. Data Cleaning, EDA and Visualizations

Run the data-cleaning and exploratory analysis script:

```bash
python analysis/clean_and_eda.py
