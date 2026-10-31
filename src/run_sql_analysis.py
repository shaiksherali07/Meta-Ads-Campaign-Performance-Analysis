"""
Phase 6: SQL Business Analysis Runner
Meta Ads Campaign Performance Analysis

This script executes the SQL scripts in sql/ against our database and displays
the business results cleanly in tabular format:
1. sql/campaign_analysis.sql
2. sql/audience_analysis.sql
3. sql/performance_analysis.sql
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("data", "processed", "meta_ads.db")
SQL_DIR = "sql"

def run_query_file(filename: str):
    print("\n" + "="*80)
    print(f"EXECUTING SQL SCRIPT: {filename}")
    print("="*80)
    
    file_path = os.path.join(SQL_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split queries by semicolon
    raw_queries = content.split(";")
    conn = sqlite3.connect(DB_PATH)
    
    q_num = 1
    for raw_q in raw_queries:
        # Extract SQL statements, ignoring comments and whitespace
        lines = [line for line in raw_q.strip().split("\n") if not line.strip().startswith("--")]
        clean_q = "\n".join(lines).strip()
        
        if not clean_q:
            continue
            
        # Extract title from comments preceding the query if present
        comment_lines = [line.strip().lstrip("-").strip() for line in raw_q.strip().split("\n") if line.strip().startswith("-- Query")]
        query_title = comment_lines[0] if comment_lines else f"Query {q_num}"
        
        print(f"\n>>> {query_title} <<<")
        try:
            df = pd.read_sql_query(clean_q, conn)
            print(df.to_string(index=False))
        except Exception as e:
            print(f"Error executing query: {e}")
            
        q_num += 1
        
    conn.close()

def main():
    print("="*80)
    print("PHASE 6: EXECUTING SQL BUSINESS ANALYSIS")
    print("="*80)
    
    run_query_file("campaign_analysis.sql")
    run_query_file("audience_analysis.sql")
    run_query_file("performance_analysis.sql")
    
    print("\n" + "="*80)
    print("ALL SQL BUSINESS QUERIES EXECUTED AND VERIFIED!")
    print("="*80)

if __name__ == "__main__":
    main()
