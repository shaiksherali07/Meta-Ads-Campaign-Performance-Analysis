-- ====================================================================
-- SQL Business Analysis: Campaign Performance
-- Project: Meta Ads Campaign Performance Analysis
-- Author: Senior Data Analyst & SQL Developer
-- Database: meta_ads_db
-- ====================================================================

-- --------------------------------------------------------------------
-- Query 1: Top 10 High-Performing Campaigns by ROAS (Return On Ad Spend)
-- Business Objective: Identify which campaigns generate the highest return
-- per dollar spent to prioritize future marketing budget allocation.
-- --------------------------------------------------------------------
SELECT 
    campaign_id,
    campaign_name,
    campaign_budget,
    total_spend,
    purchases AS total_conversions,
    revenue,
    ROUND(cpa, 2) AS cost_per_acquisition,
    ROUND(roas, 2) AS roas_multiple
FROM campaign_performance
WHERE total_spend > 0
ORDER BY roas DESC
LIMIT 10;

-- --------------------------------------------------------------------
-- Query 2: Lowest 10 Under-Performing Campaigns (Budget Drains)
-- Business Objective: Detect inefficient campaigns with low ROAS (< 1.0x)
-- and excessive CPA to pause or restructure creatives.
-- --------------------------------------------------------------------
SELECT 
    campaign_id,
    campaign_name,
    campaign_budget,
    total_spend,
    purchases AS total_conversions,
    revenue,
    ROUND(cpa, 2) AS cost_per_acquisition,
    ROUND(roas, 2) AS roas_multiple
FROM campaign_performance
WHERE total_spend > 0
ORDER BY roas ASC
LIMIT 10;

-- --------------------------------------------------------------------
-- Query 3: Budget Utilization & Pacing Analysis
-- Business Objective: Evaluate whether campaigns exhaust their planned
-- budget and calculate conversion delivery rate.
-- --------------------------------------------------------------------
SELECT 
    campaign_id,
    campaign_name,
    campaign_budget,
    total_spend,
    ROUND(budget_utilization_percent, 2) AS budget_utilization_pct,
    active_ads,
    purchases AS conversions,
    ROUND(total_spend / NULLIF(purchases, 0), 2) AS cpa,
    CASE 
        WHEN budget_utilization_percent >= 100.0 THEN 'Fully Utilized'
        WHEN budget_utilization_percent >= 80.0 THEN 'Optimal Pacing'
        ELSE 'Under-Delivered'
    END AS budget_status
FROM campaign_performance
ORDER BY total_spend DESC;

-- --------------------------------------------------------------------
-- Query 4: Campaign Funnel Efficiency using CTEs (Fact Table Direct Query)
-- Business Objective: Demonstrate multi-table JOINs and conditional
-- aggregation from raw fact transactions to calculate CTR, CR, and CPA.
-- --------------------------------------------------------------------
WITH campaign_funnel AS (
    SELECT 
        c.campaign_id,
        c.name AS campaign_name,
        c.total_budget,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS impressions,
        COUNT(CASE WHEN e.event_type = 'Click' THEN 1 END) AS clicks,
        COUNT(CASE WHEN e.event_type = 'Purchase' THEN 1 END) AS purchases
    FROM campaigns c
    INNER JOIN ads a ON c.campaign_id = a.campaign_id
    INNER JOIN ad_events e ON a.ad_id = e.ad_id
    GROUP BY c.campaign_id, c.name, c.total_budget
)
SELECT 
    campaign_id,
    campaign_name,
    total_budget,
    impressions,
    clicks,
    purchases,
    ROUND((clicks * 100.0) / NULLIF(impressions, 0), 2) AS ctr_pct,
    ROUND((purchases * 100.0) / NULLIF(clicks, 0), 2) AS conversion_rate_pct,
    ROUND(total_budget / NULLIF(purchases, 0), 2) AS cost_per_purchase
FROM campaign_funnel
ORDER BY purchases DESC
LIMIT 15;
