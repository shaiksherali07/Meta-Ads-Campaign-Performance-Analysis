-- ====================================================================
-- SQL Business Analysis: Platform & Overall Performance
-- Project: Meta Ads Campaign Performance Analysis
-- Author: Senior Data Analyst & SQL Developer
-- Database: meta_ads_db
-- ====================================================================

-- --------------------------------------------------------------------
-- Query 1: Platform Head-to-Head Comparison (Facebook vs. Instagram)
-- Business Objective: Rigorously evaluate advertising efficiency between
-- Meta platforms to guide multi-channel marketing budget allocation.
-- --------------------------------------------------------------------
SELECT 
    ad_platform,
    COUNT(ad_id) AS total_ads,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(reach) AS total_reach,
    ROUND((SUM(impressions) * 1.0) / NULLIF(SUM(reach), 0), 2) AS avg_frequency,
    SUM(clicks) AS total_clicks,
    SUM(purchases) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND((SUM(clicks) * 100.0) / NULLIF(SUM(impressions), 0), 2) AS ctr_pct,
    ROUND(SUM(ad_spend) / NULLIF(SUM(clicks), 0), 2) AS cpc,
    ROUND((SUM(ad_spend) * 1000.0) / NULLIF(SUM(impressions), 0), 2) AS cpm,
    ROUND((SUM(purchases) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS conversion_rate_pct,
    ROUND(SUM(ad_spend) / NULLIF(SUM(purchases), 0), 2) AS cpa,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas
FROM ad_performance
GROUP BY ad_platform
ORDER BY roas DESC;

-- --------------------------------------------------------------------
-- Query 2: Creative Format Performance (Video, Stories, Carousel, Image)
-- Business Objective: Compare creative media types to identify the best
-- ad format for driving high-value sales.
-- --------------------------------------------------------------------
SELECT 
    ad_type AS creative_format,
    COUNT(ad_id) AS total_ads,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(purchases) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND((SUM(clicks) * 100.0) / NULLIF(SUM(impressions), 0), 2) AS ctr_pct,
    ROUND((SUM(purchases) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS conversion_rate_pct,
    ROUND(SUM(ad_spend) / NULLIF(SUM(purchases), 0), 2) AS cpa,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas
FROM ad_performance
GROUP BY ad_type
ORDER BY roas DESC;

-- --------------------------------------------------------------------
-- Query 3: Monthly Advertising Expenditure, Revenue & ROAS Trends
-- Business Objective: Track month-over-month delivery and pacing trends
-- from raw event timestamps.
-- --------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        e.year_month,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS impressions,
        COUNT(CASE WHEN e.event_type = 'Click' THEN 1 END) AS clicks,
        COUNT(CASE WHEN e.event_type = 'Purchase' THEN 1 END) AS purchases,
        COUNT(DISTINCT e.user_id) AS reach
    FROM ad_events e
    GROUP BY e.year_month
),
monthly_financials AS (
    SELECT 
        m.year_month,
        m.impressions,
        m.reach,
        m.clicks,
        m.purchases,
        -- Total spend allocated proportionally to monthly impression volume
        ROUND((m.impressions * 1.0 / (SELECT COUNT(*) FROM ad_events WHERE event_type = 'Impression')) * 
              (SELECT SUM(campaign_budget) FROM campaign_performance), 2) AS monthly_spend,
        ROUND(m.purchases * 1850.00, 2) AS monthly_revenue
    FROM monthly_metrics m
)
SELECT 
    year_month,
    impressions,
    reach,
    clicks,
    purchases,
    monthly_spend,
    monthly_revenue,
    ROUND((clicks * 100.0) / NULLIF(impressions, 0), 2) AS ctr_pct,
    ROUND(monthly_spend / NULLIF(clicks, 0), 2) AS cpc,
    ROUND(monthly_spend / NULLIF(purchases, 0), 2) AS cpa,
    ROUND(monthly_revenue / NULLIF(monthly_spend, 0), 2) AS roas
FROM monthly_financials
ORDER BY year_month ASC;

-- --------------------------------------------------------------------
-- Query 4: Time-of-Day Engagement Patterns
-- Business Objective: Discover when users are most active to optimize
-- ad delivery scheduling (Dayparting).
-- --------------------------------------------------------------------
SELECT 
    time_of_day,
    COUNT(event_id) AS total_events,
    COUNT(CASE WHEN event_type = 'Impression' THEN 1 END) AS impressions,
    COUNT(CASE WHEN event_type = 'Click' THEN 1 END) AS clicks,
    COUNT(CASE WHEN event_type IN ('Like', 'Comment', 'Share') THEN 1 END) AS engagements,
    COUNT(CASE WHEN event_type = 'Purchase' THEN 1 END) AS purchases,
    ROUND(
        (COUNT(CASE WHEN event_type = 'Click' THEN 1 END) * 100.0) /
        NULLIF(COUNT(CASE WHEN event_type = 'Impression' THEN 1 END), 0),
        2
    ) AS ctr_pct
FROM ad_events
GROUP BY time_of_day
ORDER BY total_events DESC;

-- --------------------------------------------------------------------
-- Query 5: Executive Portfolio Summary KPI Table
-- Business Objective: Produce a single row containing overall KPIs.
-- --------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT campaign_id) AS total_campaigns,
    ROUND(SUM(campaign_budget), 2) AS total_budget,
    ROUND(SUM(total_spend), 2) AS total_spend,
    ROUND((SUM(total_spend) * 100.0) / NULLIF(SUM(campaign_budget), 0), 2) AS budget_utilization_pct,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(purchases) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND((SUM(clicks) * 100.0) / NULLIF(SUM(impressions), 0), 2) AS overall_ctr_pct,
    ROUND(SUM(total_spend) / NULLIF(SUM(clicks), 0), 2) AS overall_cpc,
    ROUND((SUM(total_spend) * 1000.0) / NULLIF(SUM(impressions), 0), 2) AS overall_cpm,
    ROUND((SUM(purchases) * 100.0) / NULLIF(SUM(clicks), 0), 2) AS overall_conversion_rate_pct,
    ROUND(SUM(total_spend) / NULLIF(SUM(purchases), 0), 2) AS overall_cpa,
    ROUND(SUM(revenue) / NULLIF(SUM(total_spend), 0), 2) AS overall_roas
FROM campaign_performance;
