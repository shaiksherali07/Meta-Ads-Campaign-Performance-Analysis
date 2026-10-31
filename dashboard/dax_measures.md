# Power BI DAX Measures Reference Guide
## Meta Ads Campaign Performance Analysis

This guide contains all production-ready Data Analysis Expressions (DAX) measures used in the Power BI dashboard.
Copy and paste these measures directly into your Power BI model.

---

### Table: `_Measures` (Dedicated Calculation Group)

> [!TIP]
> Best Practice: In Power BI, create an empty table named `_Measures` to store all calculation measures in one organized folder rather than scattering them across data tables.

---

### 1. Financial & Spend Measures

```dax
// Total Advertising Budget Allocated
Total Budget = 
SUM('campaign_performance'[campaign_budget])

// Total Actual Ad Spend
Total Spend = 
SUM('campaign_performance'[total_spend])

// Budget Utilization Percentage
Budget Utilization % = 
DIVIDE([Total Spend], [Total Budget], 0)

// Total Attributed Revenue ($1,850 per purchase benchmark)
Total Revenue = 
SUM('campaign_performance'[revenue])

// Return On Advertising Spend (ROAS Multiple)
ROAS = 
DIVIDE([Total Revenue], [Total Spend], 0)

// Net Advertising Profit ($)
Net Profit = 
[Total Revenue] - [Total Spend]
```

---

### 2. Audience Delivery & Engagement Measures

```dax
// Total Ad Impressions Delivered
Total Impressions = 
SUM('ad_performance'[impressions])

// Total Unique Audience Reach
Total Reach = 
SUM('ad_performance'[reach])

// Average Frequency (Impressions per unique user)
Ad Frequency = 
DIVIDE([Total Impressions], [Total Reach], 0)

// Total User Clicks
Total Clicks = 
SUM('ad_performance'[clicks])

// Total Engagements (Likes + Comments + Shares + Clicks)
Total Engagements = 
SUM('ad_performance'[engagements])

// Click-Through Rate (CTR %)
CTR % = 
DIVIDE([Total Clicks], [Total Impressions], 0)

// Engagement Rate (%)
Engagement Rate % = 
DIVIDE([Total Engagements], [Total Impressions], 0)
```

---

### 3. Unit Cost & Conversion Efficiency Measures

```dax
// Cost Per Click (CPC in $)
CPC = 
DIVIDE([Total Spend], [Total Clicks], 0)

// Cost Per Thousand Impressions (CPM in $)
CPM = 
DIVIDE([Total Spend], [Total Impressions], 0) * 1000

// Total Purchases (Conversions)
Total Purchases = 
SUM('ad_performance'[purchases])

// Conversion Rate (% of clicks that purchased)
Conversion Rate % = 
DIVIDE([Total Purchases], [Total Clicks], 0)

// Purchase Rate (% of impressions that purchased)
Purchase Rate % = 
DIVIDE([Total Purchases], [Total Impressions], 0)

// Cost Per Acquisition (CPA in $)
CPA = 
DIVIDE([Total Spend], [Total Purchases], 0)
```

---

### 4. Dynamic KPI Formatting & Conditional Indicators

```dax
// Dynamic ROAS Performance Status (for Badges & Alerts)
ROAS Status = 
SWITCH(
    TRUE(),
    [ROAS] >= 2.0, "High Performer (>= 2.0x)",
    [ROAS] >= 1.0, "Profitable (1.0x - 1.99x)",
    "Unprofitable (< 1.0x)"
)

// Dynamic Color Hex for Conditional Formatting
ROAS Color = 
SWITCH(
    TRUE(),
    [ROAS] >= 2.0, "#2E7D32",   // Forest Green
    [ROAS] >= 1.0, "#F7B125",   // Golden Amber
    "#D32F2F"                   // Warning Red
)
```
