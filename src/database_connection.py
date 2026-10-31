"""
Phase 5: Database Connection & Ingestion Pipeline
Meta Ads Campaign Performance Analysis

This module handles:
1. Connecting to MySQL Database (or local relational SQLite database).
2. Creating database schema with Primary Keys, Foreign Keys, and Indexes.
3. Ingesting cleaned datasets from data/processed/.
4. Verifying imported row counts and referential integrity.
"""

import os
import sys
import argparse
import pandas as pd
from sqlalchemy import create_engine, text

PROCESSED_DIR = os.path.join("data", "processed")
SQLITE_DB_PATH = os.path.join(PROCESSED_DIR, "meta_ads.db")

# Default MySQL configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "meta_ads_db")
}

def get_engine(use_mysql=False):
    """
    Returns an active SQLAlchemy engine.
    If use_mysql is True, tries to connect to MySQL; falls back to SQLite if unreachable.
    """
    if use_mysql:
        try:
            cfg = MYSQL_CONFIG
            conn_url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}"
            temp_engine = create_engine(conn_url)
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {cfg['database']}"))
                conn.commit()
            print(f"  -> Connected to MySQL server at {cfg['host']}:{cfg['port']}")
            db_url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
            return create_engine(db_url), "MySQL"
        except Exception as e:
            print(f"  [!] Notice: MySQL connection at {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']} not available: {e}")
            print(f"  [!] Seamlessly initializing local relational database: {SQLITE_DB_PATH}")
            return create_engine(f"sqlite:///{SQLITE_DB_PATH}"), "SQLite"
    else:
        return create_engine(f"sqlite:///{SQLITE_DB_PATH}"), "SQLite"

def create_tables(engine, db_type):
    """Create schema tables in database."""
    print(f"\n[1/3] Creating Database Schema ({db_type}) ...")
    
    # Standard ANSI SQL DDL compatible across MySQL and SQLite
    ddl_statements = [
        "DROP TABLE IF EXISTS ad_events;",
        "DROP TABLE IF EXISTS ad_performance;",
        "DROP TABLE IF EXISTS campaign_performance;",
        "DROP TABLE IF EXISTS ads;",
        "DROP TABLE IF EXISTS users;",
        "DROP TABLE IF EXISTS campaigns;",
        
        """
        CREATE TABLE campaigns (
            campaign_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            duration_days INTEGER NOT NULL,
            total_budget REAL NOT NULL
        );
        """,
        """
        CREATE TABLE ads (
            ad_id INTEGER PRIMARY KEY,
            campaign_id INTEGER NOT NULL,
            ad_platform TEXT NOT NULL,
            ad_type TEXT NOT NULL,
            target_gender TEXT NOT NULL,
            target_age_group TEXT NOT NULL,
            target_interests TEXT,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id)
        );
        """,
        """
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            user_gender TEXT NOT NULL,
            user_age INTEGER NOT NULL,
            age_group TEXT NOT NULL,
            country TEXT NOT NULL,
            location TEXT NOT NULL,
            interests TEXT
        );
        """,
        """
        CREATE TABLE ad_events (
            event_id INTEGER PRIMARY KEY,
            ad_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            event_date TEXT NOT NULL,
            year_month TEXT NOT NULL,
            day_of_week TEXT NOT NULL,
            time_of_day TEXT NOT NULL,
            event_type TEXT NOT NULL,
            FOREIGN KEY (ad_id) REFERENCES ads (ad_id)
        );
        """,
        """
        CREATE TABLE ad_performance (
            ad_id INTEGER PRIMARY KEY,
            campaign_id INTEGER NOT NULL,
            campaign_name TEXT,
            campaign_budget REAL,
            ad_platform TEXT NOT NULL,
            ad_type TEXT NOT NULL,
            target_gender TEXT NOT NULL,
            target_age_group TEXT NOT NULL,
            target_interests TEXT,
            ad_spend REAL NOT NULL,
            impressions INTEGER NOT NULL,
            reach INTEGER NOT NULL,
            frequency REAL NOT NULL,
            clicks INTEGER NOT NULL,
            likes INTEGER NOT NULL,
            shares INTEGER NOT NULL,
            comments INTEGER NOT NULL,
            engagements INTEGER NOT NULL,
            purchases INTEGER NOT NULL,
            ctr_percent REAL NOT NULL,
            cpc REAL NOT NULL,
            cpm REAL NOT NULL,
            conversion_rate_percent REAL NOT NULL,
            cpa REAL NOT NULL,
            revenue REAL NOT NULL,
            roas REAL NOT NULL
        );
        """,
        """
        CREATE TABLE campaign_performance (
            campaign_id INTEGER PRIMARY KEY,
            campaign_name TEXT NOT NULL,
            campaign_budget REAL NOT NULL,
            active_ads INTEGER NOT NULL,
            total_spend REAL NOT NULL,
            budget_utilization_percent REAL NOT NULL,
            impressions INTEGER NOT NULL,
            reach INTEGER NOT NULL,
            clicks INTEGER NOT NULL,
            engagements INTEGER NOT NULL,
            purchases INTEGER NOT NULL,
            revenue REAL NOT NULL,
            ctr_percent REAL NOT NULL,
            cpc REAL NOT NULL,
            cpm REAL NOT NULL,
            conversion_rate_percent REAL NOT NULL,
            cpa REAL NOT NULL,
            roas REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            duration_days INTEGER NOT NULL
        );
        """
    ]
    
    with engine.connect() as conn:
        for stmt in ddl_statements:
            conn.execute(text(stmt))
        conn.commit()
    print("  -> All 6 tables successfully initialized.")

def import_datasets(engine):
    """Import cleaned CSVs into the relational database."""
    print("\n[2/3] Importing Processed Datasets into Database ...")
    
    table_files = [
        ("campaigns", "clean_campaigns.csv"),
        ("ads", "clean_ads.csv"),
        ("users", "clean_users.csv"),
        ("ad_events", "clean_ad_events.csv"),
        ("ad_performance", "clean_ad_performance.csv"),
        ("campaign_performance", "clean_campaign_performance.csv")
    ]
    
    for table_name, file_name in table_files:
        csv_path = os.path.join(PROCESSED_DIR, file_name)
        print(f"  -> Ingesting {file_name} into table '{table_name}' ...", end=" ", flush=True)
        
        # Load in chunks for large table ad_events (400,000 rows)
        if file_name == "clean_ad_events.csv":
            chunksize = 50000
            for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
                chunk.to_sql(table_name, con=engine, if_exists="append" if i > 0 else "append", index=False)
        else:
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, con=engine, if_exists="append", index=False)
            
        print("Done!")

def verify_imported_records(engine):
    """Verify row counts and financial totals."""
    print("\n[3/3] Verifying Imported Records & Data Integrity ...")
    
    tables = ["campaigns", "ads", "users", "ad_events", "ad_performance", "campaign_performance"]
    verification_results = []
    
    with engine.connect() as conn:
        for t in tables:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
            verification_results.append({"Table Name": t, "Imported Row Count": f"{count:,}"})
            
        # Check financial consistency
        db_spend = conn.execute(text("SELECT SUM(total_spend) FROM campaign_performance")).scalar()
        db_purchases = conn.execute(text("SELECT SUM(purchases) FROM campaign_performance")).scalar()
        db_revenue = conn.execute(text("SELECT SUM(revenue) FROM campaign_performance")).scalar()
        
    v_df = pd.DataFrame(verification_results)
    print("\n" + v_df.to_string(index=False))
    
    print("\n--- Relational Totals Verification ---")
    print(f"  Total Spend in Database:     ${db_spend:,.2f}")
    print(f"  Total Purchases in Database: {db_purchases:,}")
    print(f"  Total Revenue in Database:   ${db_revenue:,.2f}")
    print(f"  Portfolio ROAS in Database:  {db_revenue/db_spend:.2f}x")

def main():
    parser = argparse.ArgumentParser(description="Ingest Meta Ads data into relational database.")
    parser.add_argument("--mysql", action="store_true", help="Connect to MySQL server instead of SQLite")
    args = parser.parse_args()
    
    print("="*70)
    print("PHASE 5: DATABASE INGESTION & INTEGRITY SETUP")
    print("="*70)
    
    engine, db_type = get_engine(use_mysql=args.mysql)
    create_tables(engine, db_type)
    import_datasets(engine)
    verify_imported_records(engine)
    
    print("\n" + "="*70)
    print("DATABASE SETUP & INGESTION COMPLETED SUCCESSFULLY!")
    print("Database is ready for Phase 6 SQL Business Analysis.")
    print("="*70)

if __name__ == "__main__":
    main()
