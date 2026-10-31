# Data Dictionary: Meta Ads Campaign Performance Analysis

## Overview
The dataset models an end-to-end digital advertising ecosystem for **Meta Platforms (Facebook & Instagram)**. It follows a **Star Schema** with one central transactional Fact Table (`ad_events`) and three Dimension Tables (`campaigns`, `ads`, `users`).

---

## 1. Dimension Table: `campaigns`
* **File**: `data/raw/campaigns.csv`
* **Total Rows**: 50
* **Primary Key**: `campaign_id`

| Column Name | Data Type (Raw) | Target Type (SQL/Cleaned) | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `campaign_id` | `int64` | `INT PRIMARY KEY` | Unique identifier for each marketing campaign | `1` |
| `name` | `object` (str) | `VARCHAR(100)` | Descriptive name/theme of the campaign | `Campaign_1_Launch` |
| `start_date` | `object` (str) | `DATE` | Campaign start date (DD-MM-YYYY in raw) | `25-05-2025` |
| `end_date` | `object` (str) | `DATE` | Campaign scheduled end date (DD-MM-YYYY in raw) | `23-07-2025` |
| `duration_days` | `int64` | `INT` | Total active lifespan of the campaign in days | `59` |
| `total_budget` | `float64` | `DECIMAL(10,2)` | Total allocated financial budget in USD | `24021.32` |

---

## 2. Dimension Table: `ads`
* **File**: `data/raw/ads.csv`
* **Total Rows**: 200
* **Primary Key**: `ad_id`
* **Foreign Key**: `campaign_id` references `campaigns(campaign_id)`

| Column Name | Data Type (Raw) | Target Type (SQL/Cleaned) | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `ad_id` | `int64` | `INT PRIMARY KEY` | Unique identifier for each individual ad creative | `1` |
| `campaign_id` | `int64` | `INT FOREIGN KEY` | Parent campaign that funds this ad creative | `28` |
| `ad_platform` | `object` (str) | `VARCHAR(50)` | Meta advertising placement platform (`Facebook`, `Instagram`) | `Facebook` |
| `ad_type` | `object` (str) | `VARCHAR(50)` | Creative media format (`Video`, `Stories`, `Carousel`, `Image`) | `Video` |
| `target_gender` | `object` (str) | `VARCHAR(20)` | Intended audience gender filter (`Male`, `Female`, `All`) | `Female` |
| `target_age_group` | `object` (str) | `VARCHAR(20)` | Target demographic age bracket (`18-24`, `25-34`, `35-44`, `45-54`) | `35-44` |
| `target_interests`| `object` (str) | `VARCHAR(255)` | Target interest keywords used in ad set configuration | `art, technology` |

---

## 3. Dimension Table: `users`
* **File**: `data/raw/users.csv`
* **Total Rows**: 9,841
* **Primary Key**: `user_id`

| Column Name | Data Type (Raw) | Target Type (SQL/Cleaned) | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `object` (str) | `VARCHAR(50) PRIMARY KEY` | Unique identifier of the Meta user | `f9c67` |
| `user_gender` | `object` (str) | `VARCHAR(20)` | Gender of the user (`Male`, `Female`, `Other`) | `Male` |
| `user_age` | `int64` | `INT` | Exact numeric age of the user (16 to 65) | `56` |
| `age_group` | `object` (str) | `VARCHAR(20)` | Standardized age demographic bucket | `55-65` |
| `country` | `object` (str) | `VARCHAR(50)` | Country where user is based | `Japan` |
| `location` | `object` (str) | `VARCHAR(100)` | City/region of the user | `New Jeremy` |
| `interests` | `object` (str) | `VARCHAR(255)` | User's profile interests | `lifestyle, health` |

---

## 4. Fact Table: `ad_events`
* **File**: `data/raw/ad_events.csv`
* **Total Rows**: 400,000
* **Primary Key**: `event_id`
* **Foreign Keys**: 
  - `ad_id` references `ads(ad_id)`
  - `user_id` references `users(user_id)`

| Column Name | Data Type (Raw) | Target Type (SQL/Cleaned) | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `event_id` | `int64` | `BIGINT PRIMARY KEY` | Unique ID for each individual interaction event | `1` |
| `ad_id` | `int64` | `INT FOREIGN KEY` | Specific ad creative displayed to user | `197` |
| `user_id` | `object` (str) | `VARCHAR(50)` | User who viewed or engaged with the ad | `2359b` |
| `timestamp` | `object` (str) | `DATETIME` | Exact date and time event occurred | `2025-07-26 00:19:56` |
| `day_of_week` | `object` (str) | `VARCHAR(20)` | Day name extracted from timestamp | `Saturday` |
| `time_of_day` | `object` (str) | `VARCHAR(20)` | Categorical time window (`Morning`, `Afternoon`, `Evening`, `Night`) | `Night` |
| `event_type` | `object` (str) | `VARCHAR(30)` | Funnel action (`Impression`, `Click`, `Like`, `Share`, `Comment`, `Purchase`) | `Like` |

---

## 5. Entity Relationship (Star Schema)

```text
       [ campaigns ] (1)
             │
             │ 1-to-Many
             ▼
          [ ads ] (1)
             │
             │ 1-to-Many
             ▼
      [ ad_events ] (Fact) ◀─── 1-to-Many ─── [ users ] (1)
```
