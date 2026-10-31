-- ====================================================================
-- Database Schema Definition
-- Project: Meta Ads Campaign Performance Analysis
-- Phase: 5 (MySQL Database Setup)
-- Author: Senior Data Analyst & SQL Developer
-- ====================================================================

-- 1. Create and Select Database
CREATE DATABASE IF NOT EXISTS meta_ads_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE meta_ads_db;

-- 2. Drop Tables if existing (in reverse dependency order)
DROP TABLE IF EXISTS ad_events;
DROP TABLE IF EXISTS ad_performance;
DROP TABLE IF EXISTS campaign_performance;
DROP TABLE IF EXISTS ads;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS campaigns;

-- ====================================================================
-- DIMENSION TABLES
-- ====================================================================

-- Dimension 1: campaigns
CREATE TABLE campaigns (
    campaign_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INT NOT NULL,
    total_budget DECIMAL(12, 2) NOT NULL,
    PRIMARY KEY (campaign_id)
) ENGINE=InnoDB;

-- Dimension 2: ads
CREATE TABLE ads (
    ad_id INT NOT NULL,
    campaign_id INT NOT NULL,
    ad_platform VARCHAR(50) NOT NULL,
    ad_type VARCHAR(50) NOT NULL,
    target_gender VARCHAR(20) NOT NULL,
    target_age_group VARCHAR(20) NOT NULL,
    target_interests VARCHAR(255),
    PRIMARY KEY (ad_id),
    CONSTRAINT fk_ads_campaign
        FOREIGN KEY (campaign_id) REFERENCES campaigns (campaign_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Dimension 3: users
CREATE TABLE users (
    user_id VARCHAR(50) NOT NULL,
    user_gender VARCHAR(20) NOT NULL,
    user_age INT NOT NULL,
    age_group VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    interests VARCHAR(255),
    PRIMARY KEY (user_id)
) ENGINE=InnoDB;

-- ====================================================================
-- FACT TABLE (TRANSACTIONAL)
-- ====================================================================

-- Fact Table: ad_events (400,000 interactions)
CREATE TABLE ad_events (
    event_id BIGINT NOT NULL,
    ad_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    event_date DATE NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    time_of_day VARCHAR(20) NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    PRIMARY KEY (event_id),
    CONSTRAINT fk_events_ad
        FOREIGN KEY (ad_id) REFERENCES ads (ad_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_events_ad_id (ad_id),
    INDEX idx_events_user_id (user_id),
    INDEX idx_events_type (event_type),
    INDEX idx_events_date (event_date),
    INDEX idx_events_year_month (year_month)
) ENGINE=InnoDB;

-- ====================================================================
-- AGGREGATED ANALYTICAL TABLES (FOR HIGH-SPEED REPORTING & BI)
-- ====================================================================

-- Aggregate 1: ad_performance (Ad Creative Level)
CREATE TABLE ad_performance (
    ad_id INT NOT NULL,
    campaign_id INT NOT NULL,
    campaign_name VARCHAR(100),
    campaign_budget DECIMAL(12, 2),
    ad_platform VARCHAR(50) NOT NULL,
    ad_type VARCHAR(50) NOT NULL,
    target_gender VARCHAR(20) NOT NULL,
    target_age_group VARCHAR(20) NOT NULL,
    target_interests VARCHAR(255),
    ad_spend DECIMAL(12, 2) NOT NULL,
    impressions INT NOT NULL,
    reach INT NOT NULL,
    frequency DECIMAL(6, 2) NOT NULL,
    clicks INT NOT NULL,
    likes INT NOT NULL,
    shares INT NOT NULL,
    comments INT NOT NULL,
    engagements INT NOT NULL,
    purchases INT NOT NULL,
    ctr_percent DECIMAL(6, 2) NOT NULL,
    cpc DECIMAL(10, 2) NOT NULL,
    cpm DECIMAL(10, 2) NOT NULL,
    conversion_rate_percent DECIMAL(6, 2) NOT NULL,
    cpa DECIMAL(10, 2) NOT NULL,
    revenue DECIMAL(12, 2) NOT NULL,
    roas DECIMAL(6, 2) NOT NULL,
    PRIMARY KEY (ad_id)
) ENGINE=InnoDB;

-- Aggregate 2: campaign_performance (Campaign Strategic Level)
CREATE TABLE campaign_performance (
    campaign_id INT NOT NULL,
    campaign_name VARCHAR(100) NOT NULL,
    campaign_budget DECIMAL(12, 2) NOT NULL,
    active_ads INT NOT NULL,
    total_spend DECIMAL(12, 2) NOT NULL,
    budget_utilization_percent DECIMAL(6, 2) NOT NULL,
    impressions INT NOT NULL,
    reach INT NOT NULL,
    clicks INT NOT NULL,
    engagements INT NOT NULL,
    purchases INT NOT NULL,
    revenue DECIMAL(12, 2) NOT NULL,
    ctr_percent DECIMAL(6, 2) NOT NULL,
    cpc DECIMAL(10, 2) NOT NULL,
    cpm DECIMAL(10, 2) NOT NULL,
    conversion_rate_percent DECIMAL(6, 2) NOT NULL,
    cpa DECIMAL(10, 2) NOT NULL,
    roas DECIMAL(6, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INT NOT NULL,
    PRIMARY KEY (campaign_id)
) ENGINE=InnoDB;
