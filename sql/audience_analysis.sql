-- ====================================================================
-- SQL Business Analysis: Audience & Demographics
-- Project: Meta Ads Campaign Performance Analysis
-- Author: Senior Data Analyst & SQL Developer
-- Database: meta_ads_db
-- ====================================================================

-- --------------------------------------------------------------------
-- Query 1: Performance by Target Age Group
-- Business Objective: Determine which age bracket generates the highest
-- conversion efficiency, lowest CPA, and greatest ROAS.
-- --------------------------------------------------------------------
SELECT 
    target_age_group,
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
GROUP BY target_age_group
ORDER BY roas DESC;

-- --------------------------------------------------------------------
-- Query 2: Performance by Target Gender
-- Business Objective: Compare ad spend efficiency across Male, Female,
-- and Unisex (All) audience targeting segments.
-- --------------------------------------------------------------------
SELECT 
    target_gender,
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
GROUP BY target_gender
ORDER BY roas DESC;

-- --------------------------------------------------------------------
-- Query 3: Geographic Distribution (Country-Level Reach & Purchases)
-- Business Objective: Connect raw ad events with user demographic profiles
-- to evaluate international reach, engagement volume, and purchases.
-- --------------------------------------------------------------------
SELECT 
    u.country,
    COUNT(DISTINCT u.user_id) AS total_users,
    COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS total_impressions,
    COUNT(CASE WHEN e.event_type = 'Click' THEN 1 END) AS total_clicks,
    COUNT(CASE WHEN e.event_type IN ('Like', 'Comment', 'Share') THEN 1 END) AS total_engagements,
    COUNT(CASE WHEN e.event_type = 'Purchase' THEN 1 END) AS total_purchases,
    ROUND(
        (COUNT(CASE WHEN e.event_type = 'Purchase' THEN 1 END) * 100.0) /
        NULLIF(COUNT(CASE WHEN e.event_type = 'Click' THEN 1 END), 0),
        2
    ) AS click_to_purchase_rate_pct
FROM users u
INNER JOIN ad_events e ON u.user_id = e.user_id
GROUP BY u.country
ORDER BY total_purchases DESC;

-- --------------------------------------------------------------------
-- Query 4: Audience Age Bracket Cross-Tabulation with Creative Formats
-- Business Objective: Identify which creative format (e.g. Stories vs Video)
-- resonates best with young (18-24) vs older (35-44) segments.
-- --------------------------------------------------------------------
SELECT 
    target_age_group,
    ad_type AS creative_format,
    COUNT(ad_id) AS active_ads,
    ROUND(SUM(ad_spend), 2) AS spend,
    SUM(purchases) AS purchases,
    ROUND(SUM(ad_spend) / NULLIF(SUM(purchases), 0), 2) AS cpa,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas
FROM ad_performance
GROUP BY target_age_group, ad_type
ORDER BY target_age_group, roas DESC;
