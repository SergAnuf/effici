# src/analyze_results.py
import os
import sqlite3
import pandas as pd
from config import OUTPUT_DIR

def analyze_output():
    sql_path = os.path.join(OUTPUT_DIR, "eplusout.sql")
    con = sqlite3.connect(sql_path)
    cur = con.cursor()
    required_tables = {"ReportData", "ReportDataDictionary"}
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = {row[0] for row in cur.fetchall()}
    if not required_tables.issubset(existing_tables):
        raise RuntimeError(f"Missing required tables: {required_tables - existing_tables}")
    query = """
    SELECT rdd.Name, rd.Value
    FROM ReportData rd
    JOIN ReportDataDictionary rdd
    ON rd.ReportDataDictionaryIndex = rdd.ReportDataDictionaryIndex
    WHERE rdd.ReportingFrequency = 'Annual'
    AND rdd.Name IN ('Electricity:Facility', 'NaturalGas:Facility')
    """
    df = pd.read_sql_query(query, con)
    con.close()
    print("\nAnnual Energy Use (GJ):")
    print(df)

if __name__ == "__main__":
    analyze_output()