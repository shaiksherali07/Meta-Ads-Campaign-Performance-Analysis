# Power BI Dashboard Specification & Build Guide
## Meta Ads Campaign Performance Analysis

This document provides the exact field mappings, visual configurations, interactive slicers, and formatting guides for building the 4-page Power BI dashboard.

---

## Data Model Configuration (Star Schema)

In Power BI Desktop:
1. Click **Get Data** $\rightarrow$ **Text/CSV** (or **MySQL Database** / **Folder**).
2. Load the following files from `data/processed/`:
   - `clean_campaigns.csv` $\rightarrow$ Name: `campaigns`
   - `clean_ads.csv` $\rightarrow$ Name: `ads`
   - `clean_users.csv` $\rightarrow$ Name: `users`
   - `clean_ad_events.csv` $\rightarrow$ Name: `ad_events`
   - `clean_ad_performance.csv` $\rightarrow$ Name: `ad_performance`
   - `clean_campaign_performance.csv` $\rightarrow$ Name: `campaign_performance`
   - `clean_daily_performance.csv` $\rightarrow$ Name: `daily_performance`
3. Establish Relationships in **Model View**:
   - `campaigns[campaign_id]` (1) $\rightarrow$ `ads[campaign_id]` (*)
   - `ads[ad_id]` (1) $\rightarrow$ `ad_events[ad_id]` (*)
   - `users[user_id]` (1) $\rightarrow$ `ad_events[user_id]` (*)
   - `campaign_performance[campaign_id]` (1) $\rightarrow$ `ad_performance[campaign_id]` (*)

---

## Color Palette & Theme Styling
- **Background**: Soft Gray (`#F8F9FA`)
- **Primary Meta Blue**: `#1877F2`
- **Instagram Rose / Magenta**: `#E1306C`
- **Success / Revenue Green**: `#2E7D32`
- **Warning / Spend Amber**: `#E64A19`
- **Alert / Inefficiency Red**: `#D32F2F`
- **Card Background**: Pure White (`#FFFFFF`) with subtle shadow and 8px corner radius.

---

## Page 1: Executive Overview

**Objective:** High-level executive pulse check summarizing overall delivery, revenue, spend pacing, and platform distribution.

### 1. Global Slicers (Top Banner)
- **Date Slicer**: `daily_performance[event_date]` (Between: `2025-05-07` to `2025-08-06`).
- **Platform Dropdown**: `ads[ad_platform]` (All, Facebook, Instagram).
- **Campaign Dropdown**: `campaigns[name]` (Searchable multiselect).

### 2. Top KPI Cards (6 Horizontal Cards)
| Card Label | Measure / Field | Display Format | Target Value |
| :--- | :--- | :--- | :--- |
| **Total Spend** | `[Total Spend]` | Currency (`$#,##0`) | **$2,383,052** |
| **Total Impressions** | `[Total Impressions]` | Whole Number (`#,##0`) | **339,812** |
| **Total Reach** | `[Total Reach]` | Whole Number (`#,##0`) | **312,127** |
| **Total Clicks** | `[Total Clicks]` | Whole Number (`#,##0`) | **40,079** (CTR: 11.79%) |
| **Total Purchases** | `[Total Purchases]` | Whole Number (`#,##0`) | **2,031** (CR: 5.07%) |
| **Total Revenue** | `[Total Revenue]` | Currency (`$#,##0`) | **$3,757,350** (**1.58x ROAS**) |

### 3. Visuals & Layout
- **Visual 1 (Line & Clustered Column Chart)**: *Monthly Advertising Spend vs. Revenue*
  - **X-Axis**: `daily_performance[year_month]`
  - **Column Y-Axis**: `[Total Spend]`, `[Total Revenue]`
  - **Line Y-Axis**: `[ROAS]`
- **Visual 2 (Donut Chart)**: *Spend & Conversion Share by Platform*
  - **Legend**: `ad_performance[ad_platform]`
  - **Values**: `[Total Spend]` (or toggle to `[Total Purchases]`)
  - **Callout Value**: Percent of total (Facebook: 61.4%, Instagram: 38.6%).
- **Visual 3 (Table / Matrix)**: *Top 5 High-Impact Campaigns*
  - **Columns**: `campaign_name`, `total_spend`, `purchases`, `revenue`, `cpa`, `roas`
  - **Data Bars**: Applied to `roas` column.

---

## Page 2: Campaign Performance

**Objective:** Detailed campaign-level diagnostics to compare top vs. bottom performers, evaluate pacing, and audit budget utilization.

### 1. Header & Quick Metrics
- **Active Campaigns**: `COUNTROWS(campaign_performance)` $\rightarrow$ **48**
- **Avg Budget per Campaign**: `AVERAGE(campaign_performance[campaign_budget])` $\rightarrow$ **$49,647**
- **Budget Utilization**: `[Budget Utilization %]` $\rightarrow$ **100.00%**

### 2. Visuals & Layout
- **Visual 1 (Horizontal Bar Chart)**: *Top 10 Campaigns by ROAS*
  - **Y-Axis**: `campaign_performance[campaign_name]`
  - **X-Axis**: `[ROAS]`
  - **Data Labels**: On (Values: `15.65x`, `5.43x`, `5.42x`, `5.29x`, `4.82x`...)
  - **Color**: Gradient Green.
- **Visual 2 (Horizontal Bar Chart)**: *Lowest 10 Campaigns by ROAS (Budget Drains)*
  - **Y-Axis**: `campaign_performance[campaign_name]`
  - **X-Axis**: `[ROAS]`
  - **Color**: Coral / Red (`0.28x`, `0.31x`, `0.31x`, `0.61x`...)
- **Visual 3 (Scatter Plot / Quadrant Analysis)**: *Spend vs. ROAS Analysis*
  - **X-Axis**: `total_spend`
  - **Y-Axis**: `roas`
  - **Size**: `purchases`
  - **Legend**: `campaign_name`
  - **Reference Lines**: X-Average Spend ($49.6K), Y-Breakeven ROAS (1.0x).
- **Visual 4 (Table with Conditional Formatting)**: *Campaign Pacing & Conversion Matrix*
  - **Columns**: `campaign_name`, `duration_days`, `total_budget`, `total_spend`, `budget_utilization_pct`, `purchases`, `cpa`, `roas`
  - **Conditional Rules**: Background color on `roas` (Red < 1.0, Green >= 2.0).

---

## Page 3: Audience Analysis

**Objective:** Profile consumer demographics, geographic reach, and audience engagement affinity across age and gender cohorts.

### 1. Visuals & Layout
- **Visual 1 (Clustered Column Chart)**: *Performance by Target Age Group*
  - **X-Axis**: `ad_performance[target_age_group]` (`18-24`, `25-34`, `35-44`, `All`)
  - **Y-Axis**: `[Total Purchases]`
  - **Secondary Line**: `[ROAS]`
  - **Key takeaway**: Age 18–24 delivers top ROAS (1.74x) and lowest CPA ($1,065).
- **Visual 2 (Donut Chart)**: *Conversions by Target Gender*
  - **Legend**: `ad_performance[target_gender]` (`Female`, `All`, `Male`)
  - **Values**: `[Total Purchases]`
  - **Insight**: Female targeting generates 40.2% of all conversions.
- **Visual 3 (Filled Map or Horizontal Bar Chart)**: *Top Converting Countries*
  - **Location**: `users[country]`
  - **Size / Values**: `COUNT(ad_events[event_id])` filtered by `event_type = 'Purchase'`
  - **Top Countries**: United States (645), United Kingdom (283), Canada (194), India (185), Germany (150).
- **Visual 4 (Matrix / Heatmap)**: *Age Group vs. Creative Format Cross-Tabulation*
  - **Rows**: `target_age_group`
  - **Columns**: `ad_type` (`Stories`, `Carousel`, `Video`, `Image`)
  - **Values**: `[ROAS]`
  - **Highlight**: 18–24 + Stories delivers peak ROAS of **2.11x**.

---

## Page 4: Conversion & ROI Analysis

**Objective:** Deep-dive into marketing efficiency, creative media formats, conversion funnel drop-offs, and dayparting.

### 1. Visuals & Layout
- **Visual 1 (Funnel Chart)**: *Meta Ads Conversion Waterfall*
  - **Category**: `ad_events[event_type]`
  - **Values**: `COUNT(event_id)`
  - **Stages**: Impressions (339,812) $\rightarrow$ Clicks (40,079) $\rightarrow$ Engagements (18,078) $\rightarrow$ Purchases (2,031).
- **Visual 2 (Clustered Bar Chart)**: *Creative Media Format Effectiveness*
  - **Y-Axis**: `ad_performance[ad_type]` (`Stories`, `Carousel`, `Video`, `Image`)
  - **X-Axis**: `[ROAS]`, `[CPA]`
  - **Data Labels**: On (Stories: 1.79x ROAS, Carousel: 1.76x, Video: 1.47x, Image: 1.28x).
- **Visual 3 (Stacked Area / Heatmap)**: *Dayparting (Hourly & Time-of-Day Engagement)*
  - **X-Axis**: `ad_events[time_of_day]` (`Night`, `Morning`, `Afternoon`, `Evening`)
  - **Y-Axis**: `COUNT(ad_events[event_id])`
  - **Color / Legend**: `event_type` (`Impression`, `Click`, `Purchase`)
- **Visual 4 (Card Cluster / Gauge)**: *Efficiency Benchmarks*
  - **Gauge 1**: CPA (Current: $1,173.34 vs. Target: $1,000.00)
  - **Gauge 2**: ROAS (Current: 1.58x vs. Target: 2.00x)
