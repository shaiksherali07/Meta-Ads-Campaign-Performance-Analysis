"""
Phase 2: Data Collection & Profiling Script
Meta Ads Campaign Performance Analysis

This script inspects the raw datasets:
1. campaigns.csv
2. ads.csv
3. users.csv
4. ad_events.csv

Checks performed:
- Table dimensions (rows, columns)
- Column data types
- Missing values (Nulls/NaNs)
- Duplicate rows
- Cardinality & primary/foreign key integrity
- Event distributions & date spans
"""

import os
import pandas as pd
import numpy as np

RAW_DATA_DIR = os.path.join("data", "raw")

def profile_dataset(file_name):
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    print(f"\n{'='*70}")
    print(f"PROFILING: {file_name}")
    print(f"{'='*70}")
    
    df = pd.read_csv(file_path, low_memory=False)
    
    # 1. Basic shape
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"\nColumns: {list(df.columns)}")
    
    # 2. Data types & Missing values
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    
    profiling_df = pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Non-Null Count": df.notnull().sum(),
        "Missing Count": missing_counts,
        "Missing %": missing_pct.round(2),
        "Unique Values": df.nunique()
    })
    print("\n--- Column Profiling ---")
    print(profiling_df.to_string())
    
    # 3. Duplicate rows check
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate Rows: {duplicates} ({(duplicates / len(df) * 100):.2f}%)")
    
    # 4. Preview first 3 rows
    print("\n--- Sample Data (First 3 Rows) ---")
    print(df.head(3).to_string())
    
    return df

def main():
    print("Starting Phase 2 Data Profiling...")
    
    campaigns_df = profile_dataset("campaigns.csv")
    ads_df = profile_dataset("ads.csv")
    users_df = profile_dataset("users.csv")
    events_df = profile_dataset("ad_events.csv")
    
    # 5. Relationship & Referential Integrity Checks
    print(f"\n{'='*70}")
    print("RELATIONSHIP & INTEGRITY VERIFICATION")
    print(f"{'='*70}")
    
    # Check 1: ads.campaign_id -> campaigns.campaign_id
    ads_campaign_ids = set(ads_df["campaign_id"].unique())
    campaign_ids = set(campaigns_df["campaign_id"].unique())
    orphan_campaigns = ads_campaign_ids - campaign_ids
    print(f"Campaigns in 'campaigns.csv': {len(campaign_ids)}")
    print(f"Campaigns referenced in 'ads.csv': {len(ads_campaign_ids)}")
    print(f"Orphan Campaign IDs in ads.csv: {orphan_campaigns if orphan_campaigns else 'None (100% Valid)'}")
    
    # Check 2: ad_events.ad_id -> ads.ad_id
    events_ad_ids = set(events_df["ad_id"].unique())
    ads_ids = set(ads_df["ad_id"].unique())
    orphan_ads = events_ad_ids - ads_ids
    print(f"\nAds in 'ads.csv': {len(ads_ids)}")
    print(f"Ads referenced in 'ad_events.csv': {len(events_ad_ids)}")
    print(f"Orphan Ad IDs in ad_events.csv: {orphan_ads if orphan_ads else 'None (100% Valid)'}")
    
    # Check 3: ad_events.user_id -> users.user_id
    events_user_ids = set(events_df["user_id"].astype(str).unique())
    users_user_ids = set(users_df["user_id"].astype(str).unique())
    orphan_users = events_user_ids - users_user_ids
    print(f"\nUsers in 'users.csv': {len(users_user_ids)}")
    print(f"Users referenced in 'ad_events.csv': {len(events_user_ids)}")
    print(f"Orphan User IDs in ad_events.csv count: {len(orphan_users)} ({(len(orphan_users)/len(events_user_ids)*100):.2f}%)")
    
    # 6. Event Breakdown
    print(f"\n{'='*70}")
    print("EVENT TYPE BREAKDOWN (ad_events.csv)")
    print(f"{'='*70}")
    event_counts = events_df["event_type"].value_counts()
    event_pct = (events_df["event_type"].value_counts(normalize=True) * 100).round(2)
    event_summary = pd.DataFrame({"Count": event_counts, "Percentage (%)": event_pct})
    print(event_summary.to_string())
    
    # 7. Date Ranges
    print(f"\n{'='*70}")
    print("DATE RANGES & SPAN")
    print(f"{'='*70}")
    print(f"Campaign start date range: {campaigns_df['start_date'].min()} to {campaigns_df['start_date'].max()}")
    print(f"Ad events timestamp range: {events_df['timestamp'].min()} to {events_df['timestamp'].max()}")

if __name__ == "__main__":
    main()
