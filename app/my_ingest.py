import os
import requests
import gzip
import ijson
import psycopg2

def clean_entry(entry):
    desc = entry.get("description", "").strip()
    entry["description"] = desc
    entry["is_other"] = desc.lower() == "other"
    return entry

def process_hts(url, conn):
    with conn.cursor() as cur:
        resp = requests.get(url, stream=True)
        gz = gzip.GzipFile(fileobj=resp.raw)
        for item in ijson.items(gz, 'item'):
            row = clean_entry(item)
            cur.execute(
                """
                INSERT INTO hts_data (htsno, indent, description, general, special, is_other)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (htsno) DO NOTHING;
                """,
                (
                    row.get('htsno'),
                    int(row.get('indent', 0)),
                    row.get('description'),
                    row.get('general'),
                    row.get('special'),
                    row.get('is_other')
                )
            )
    conn.commit()
    print("Done.")

if __name__ == "__main__":
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    process_hts("https://www.usitc.gov/sites/default/files/tata/hts/hts_2025_revision_15_json.json", conn)
    conn.close()
