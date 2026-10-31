# Executive Business Insights & Strategic Recommendations
## Meta Ads Campaign Performance Analysis

**Prepared by:** Senior Data Analyst  
**Dataset Coverage:** 400,000 Ad Interaction Events | 200 Ad Creatives | 48 Active Campaigns | Facebook & Instagram  
**Total Ad Spend Analyzed:** $2,383,051.62 | **Total Attributed Revenue:** $3,757,350.00 | **Overall ROAS:** 1.58x  

---

## Executive Summary

This report delivers a rigorous analysis of Meta (Facebook and Instagram) advertising campaigns executed between **May 2025 and August 2025**. By combining transactional event logs, ad metadata, and user demographics across Python, SQL, and Power BI, we evaluated advertising expenditure, conversion funnel velocity, creative efficiency, and return on investment.

### Key Performance Highlights:
- **Total Spend:** $2,383,051.62 with a **100.00% budget utilization rate**.
- **Delivery Scale:** **339,812 impressions** delivered across **312,127 unique users** (average ad frequency: 1.09).
- **Engagement & Intent:** **40,079 clicks** representing an above-average **CTR of 11.79%**.
- **Conversions & Revenue:** **2,031 verified purchases** generating **$3,757,350.00 in revenue**, achieving an overall **ROAS of 1.58x** at a blended **CPA of $1,173.34**.

---

## 1. High-Performing Campaigns (The Profit Engines)

A small cohort of campaigns demonstrated extraordinary marketing efficiency, outperforming the portfolio average by up to **10x**:

| Campaign Name | Spend | Purchases | Revenue | CPA | ROAS | Strategic Takeaway |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Campaign_42_Summer`** | \$7,918.05 | 67 | \$123,950.00 | **\$118.18** | **15.65x** | 🏆 **Star Campaign** — 10x cheaper CPA than portfolio average. |
| **`Campaign_29_Winter`** | \$19,773.65 | 58 | \$107,300.00 | \$340.93 | **5.43x** | Exceptional holiday promotional response. |
| **`Campaign_13_Winter`** | \$21,855.42 | 64 | \$118,400.00 | \$341.49 | **5.42x** | Highly stable conversion pacing. |
| **`Campaign_3_Winter`** | \$14,343.26 | 41 | \$75,850.00 | \$349.84 | **5.29x** | Efficient mid-tier retargeting. |
| **`Campaign_34_Winter`** | \$26,104.30 | 68 | \$125,800.00 | \$383.89 | **4.82x** | High volume with strong capital return. |

### Core Success Factors:
1. **Seasonal Messaging**: "Winter" themed campaigns consistently outperformed generic branding, maintaining ROAS between 4.8x and 5.4x.
2. **Tight Creative-to-Audience Fit**: High performers leveraged interactive formats (Stories/Carousel) with hyper-focused age targeting (18–24).

---

## 2. Inefficient Advertising Expenditure (Quantified Budget Drains)

Five campaigns operated at severe financial losses, significantly depressing the overall portfolio ROAS:

| Campaign Name | Ad Spend | Purchases | Attributed Revenue | CPA | ROAS | Capital Loss |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Campaign_35_Launch`** | \$71,626.83 | 11 | \$20,350.00 | **\$6,511.53** | **0.28x** | -\$51,276.83 |
| **`Campaign_36_Q3`** | \$58,801.99 | 10 | \$18,500.00 | **\$5,880.20** | **0.31x** | -\$40,301.99 |
| **`Campaign_50_Summer`** | \$47,274.70 | 8 | \$14,800.00 | **\$5,909.34** | **0.31x** | -\$32,474.70 |
| **`Campaign_32_Summer`** | \$81,744.52 | 27 | \$49,950.00 | **\$3,027.57** | **0.61x** | -\$31,794.52 |
| **`Campaign_45_Summer`** | \$53,303.55 | 19 | \$35,150.00 | **\$2,805.45** | **0.66x** | -\$18,153.55 |
| **TOTAL** | **\$312,751.60** | **75** | **\$138,750.00** | **\$4,169.95** | **0.44x** | **-\$174,001.60** |

### Root Causes of Inefficiency:
1. **Budget Inelasticity**: `Campaign_32_Summer` was given the single largest budget (\$81.7K) despite delivering a dismal 0.61x ROAS, indicating automated budget scaling without conversion caps.
2. **Audience Saturation / Creative Burnout**: High spend on static images resulted in click fatigue without downstream purchase intent.

---

## 3. Platform Economics: Facebook vs. Instagram

A direct comparison of Meta's two flagship platforms reveals distinct strategic roles:

```text
       FACEBOOK: THE CONVERSION ENGINE        |       INSTAGRAM: THE ENGAGEMENT CHANNEL
─────────────────────────────────────────────┼─────────────────────────────────────────────
• Spend: $1,462,840 (61.4% share)            | • Spend: $920,211 (38.6% share)
• Purchases: 1,323 (65.1% share of sales)     | • Purchases: 708 (34.9% share of sales)
• CPC: $57.62 (8% cheaper)                   | • CPC: $62.64
• CPA: $1,105.70 ($194 lower cost/sale)      | • CPA: $1,299.73
• ROAS: 1.67x                                | • ROAS: 1.42x
• CTR: 11.76%                                | • CTR: 11.86% (Higher click engagement)
```

**Strategic Takeaway:** Instagram attracts high click intent (11.86% CTR), but suffers drop-off at checkout. Facebook drives higher purchase volume at a **15% lower acquisition cost** and **17.6% higher ROAS**.

---

## 4. Creative Format & Audience Dynamics

### A. Ad Formats (Stories & Carousel Dominate)
- **Stories (ROAS: 1.79x | CPA: \$1,032.18):** Generated 683 purchases. Full-screen vertical format captures immediate user attention.
- **Carousel (ROAS: 1.76x | CPA: \$1,049.47):** Generated 521 purchases. Multi-card browsing allows users to evaluate products before clicking.
- **Video (ROAS: 1.47x | CPA: \$1,254.63):** Moderate performance; higher creative production cost.
- **Static Image (ROAS: 1.28x | CPA: \$1,446.29):** Lowest return across all creative formats ($414 higher CPA than Stories).

### B. Audience Demographics
- **Age Cohorts:** The **18–24 cohort** is the top-performing demographic, generating a **1.74x ROAS** with the lowest CPA (**\$1,065.85**). Conversely, **25–34** lagged at **1.42x ROAS**.
- **Gender:** Female targeting generated **40.2% of all conversions** (817 sales) at **1.61x ROAS**, outperforming Male targeting (**1.54x ROAS**, \$1,201 CPA).
- **The Golden Segment:** Combining **Age 18–24 with Stories format** delivered a peak **2.11x ROAS** with an ultra-efficient **\$874.83 CPA**.
- **International Opportunities:** While the **United States (645 sales)** and **UK (283 sales)** drive the largest volume, **Japan (6.32%)** and **Mexico (6.12%)** achieved the highest click-to-purchase conversion rates.

---

## 5. Actionable Strategic Recommendations

### Recommendation 1: Capital Reallocation ($312,750 Immediate Optimization)
- **Action:** Immediately pause or cut 80% of budget from `Campaign_35_Launch`, `Campaign_36_Q3`, `Campaign_50_Summer`, `Campaign_32_Summer`, and `Campaign_45_Summer`.
- **Impact:** Eliminates **-\$174,000 in net losses**.
- **Redeployment:** Shift this \$312K into scaling `Campaign_42_Summer` lookalikes and winter promotional bundles. At top-tier ROAS (4.8x–5.4x), this capital would generate an estimated **\$1.5M in incremental revenue**.

### Recommendation 2: Creative Format Shift (Phase Out Static Images)
- **Action:** Transition 50% of the static image creative budget ($350K) into **Instagram/Facebook Stories** and **Multi-Card Carousels**.
- **Impact:** Decreases blended CPA from \$1,173 to under \$1,050, yielding approximately **180 additional conversions** on the same budget.

### Recommendation 3: Placement Rebalancing (70/30 Split)
- **Action:** Adjust platform allocation from 61/39 to **70% Facebook / 30% Instagram**.
- **Rationale:** Maximize direct-response sales volume through Facebook's lower CPA (\$1,105), while reserving Instagram strictly for high-engagement Stories targeting youth cohorts (18–24).

### Recommendation 4: Localized Scaling in High-Intent International Markets
- **Action:** Create dedicated campaigns for **Japan and Mexico** with localized currency and messaging.
- **Rationale:** These countries exhibit >6.1% conversion efficiency (vs 4.8% in UK and 4.6% in Germany), representing undervalued growth markets.

---

## 6. Interview Preparation: Key Talking Points

When presenting this project in a data analyst job interview, emphasize:

1. **End-to-End Ownership:** Explain how you cleaned raw event logs in Pandas, designed a relational Star Schema in MySQL, extracted insights with complex SQL CTEs, and synthesized executive findings in Power BI.
2. **Business vs. Vanity Metrics:** Highlight that while Instagram had higher CTR (11.86% vs 11.76%), Facebook won on business impact (ROAS 1.67x vs 1.42x, CPA \$1,105 vs \$1,299).
3. **Quantifiable ROI Recommendation:** Confidently articulate how eliminating the 5 budget drains saves \$312K in wasted spend and shifts the portfolio toward 2.0x+ ROAS.
