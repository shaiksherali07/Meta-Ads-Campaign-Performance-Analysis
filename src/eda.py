"""
Phase 4: Exploratory Data Analysis (EDA) Module
Meta Ads Campaign Performance Analysis

This module performs statistical analysis and creates executive visualizations:
1. Executive KPIs Summary & Conversion Funnel
2. Monthly Advertising & Spend Trends
3. Platform Performance Comparison (Facebook vs Instagram)
4. Top & Bottom Performing Campaigns (by ROAS, Spend, and Conversions)
5. Ad Format & Creative Performance (Video, Stories, Carousel, Image)
6. Audience Demographics & Targeting Analysis (Age Groups, Gender, Interests)

All charts are exported to reports/figures/ for reporting and dashboard design.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROCESSED_DIR = os.path.join("data", "processed")
FIGURES_DIR = os.path.join("reports", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Set professional corporate visualization styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "bold",
    "figure.titlesize": 15,
    "figure.titleweight": "bold",
    "figure.dpi": 300
})

def load_data():
    """Load all processed datasets."""
    campaigns = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_campaign_performance.csv"))
    ads = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_ad_performance.csv"))
    daily = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_daily_performance.csv"))
    users = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_users.csv"))
    events = pd.read_csv(os.path.join(PROCESSED_DIR, "clean_ad_events.csv"))
    return campaigns, ads, daily, users, events

def plot_conversion_funnel(events):
    """Plot 1: Full-Funnel Conversion Waterfall."""
    print("  -> Generating Figure 1: conversion_funnel.png ...")
    
    funnel_stages = [
        ("Impressions", (events["event_type"] == "Impression").sum(), "#1877F2"),
        ("Clicks", (events["event_type"] == "Click").sum(), "#42B72A"),
        ("Engagements", events["event_type"].isin(["Like", "Comment", "Share"]).sum(), "#F7B125"),
        ("Purchases (Conversions)", (events["event_type"] == "Purchase").sum(), "#FA383E")
    ]
    
    stages = [s[0] for s in funnel_stages]
    counts = [s[1] for s in funnel_stages]
    colors = [s[2] for s in funnel_stages]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(stages[::-1], counts[::-1], color=colors[::-1], height=0.55, edgecolor="black", linewidth=0.8)
    
    # Add data labels with volume and conversion percentages
    max_val = counts[0]
    for bar in bars:
        w = bar.get_width()
        pct = (w / max_val) * 100
        ax.text(
            w + (max_val * 0.015),
            bar.get_y() + bar.get_height() / 2,
            f"{int(w):,} ({pct:.2f}% of Impr)",
            ha="left",
            va="center",
            fontweight="bold",
            fontsize=10
        )
        
    ax.set_xlim(0, max_val * 1.25)
    ax.set_title("Meta Ads Conversion Funnel: Awareness to Purchase")
    ax.set_xlabel("Event Volume")
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "conversion_funnel.png")
    plt.savefig(fig_path)
    plt.close()

def plot_monthly_trends(daily):
    """Plot 2: Monthly Advertising Expenditure & Performance Trends."""
    print("  -> Generating Figure 2: monthly_ad_trends.png ...")
    
    monthly = daily.groupby("year_month").agg(
        spend=("spend", "sum"),
        revenue=("revenue", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum")
    ).reset_index()
    
    monthly["roas"] = (monthly["revenue"] / monthly["spend"]).round(2)
    monthly["ctr_percent"] = ((monthly["clicks"] / monthly["impressions"]) * 100).round(2)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Spend vs Revenue Bar Chart
    x = np.arange(len(monthly))
    width = 0.35
    
    b1 = ax1.bar(x - width/2, monthly["spend"] / 1e3, width, label="Ad Spend ($K)", color="#E64A19", edgecolor="black", linewidth=0.5)
    b2 = ax1.bar(x + width/2, monthly["revenue"] / 1e3, width, label="Revenue ($K)", color="#2E7D32", edgecolor="black", linewidth=0.5)
    
    ax1.set_title("Monthly Advertising Spend vs. Revenue ($ in Thousands)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["year_month"])
    ax1.set_ylabel("USD ($ Thousands)")
    ax1.legend(loc="upper left")
    
    # Add values on top of bars
    for bar in b1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 15, f"${h:.0f}K", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for bar in b2:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 15, f"${h:.0f}K", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax1.set_ylim(0, (monthly["revenue"].max() / 1e3) * 1.2)
    
    # Right: Monthly ROAS & CTR Line Trend
    ax2_twin = ax2.twinx()
    l1 = ax2.plot(monthly["year_month"], monthly["roas"], color="#1565C0", marker="o", linewidth=2.5, label="ROAS (Return on Spend)")
    l2 = ax2_twin.plot(monthly["year_month"], monthly["ctr_percent"], color="#8E24AA", marker="s", linewidth=2.5, linestyle="--", label="CTR (%)")
    
    ax2.set_title("Monthly ROAS Efficiency vs. CTR (%)")
    ax2.set_ylabel("ROAS Multiple (x)", color="#1565C0", fontweight="bold")
    ax2_twin.set_ylabel("Click-Through Rate (%)", color="#8E24AA", fontweight="bold")
    ax2.set_ylim(0, monthly["roas"].max() * 1.3)
    ax2_twin.set_ylim(0, monthly["ctr_percent"].max() * 1.3)
    
    # Combined legend
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc="upper right")
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "monthly_ad_trends.png")
    plt.savefig(fig_path)
    plt.close()

def plot_platform_comparison(ads):
    """Plot 3: Facebook vs Instagram Performance Comparison."""
    print("  -> Generating Figure 3: platform_performance_comparison.png ...")
    
    platform_df = ads.groupby("ad_platform").agg(
        total_spend=("ad_spend", "sum"),
        total_revenue=("revenue", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum")
    ).reset_index()
    
    platform_df["ctr_percent"] = (platform_df["clicks"] / platform_df["impressions"]) * 100
    platform_df["cpc"] = platform_df["total_spend"] / platform_df["clicks"]
    platform_df["cpa"] = platform_df["total_spend"] / platform_df["purchases"]
    platform_df["roas"] = platform_df["total_revenue"] / platform_df["total_spend"]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    colors = ["#1877F2", "#E1306C"]  # Facebook Blue, Instagram Gradient Pink
    
    # 1. Total Spend vs Revenue
    x = np.arange(len(platform_df))
    w = 0.35
    axes[0, 0].bar(x - w/2, platform_df["total_spend"] / 1e3, w, label="Spend ($K)", color="#EF5350", edgecolor="black", linewidth=0.5)
    axes[0, 0].bar(x + w/2, platform_df["total_revenue"] / 1e3, w, label="Revenue ($K)", color="#66BB6A", edgecolor="black", linewidth=0.5)
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(platform_df["ad_platform"])
    axes[0, 0].set_title("Total Spend vs. Revenue ($K)")
    axes[0, 0].legend()
    for i, row in platform_df.iterrows():
        axes[0, 0].text(i - w/2, (row["total_spend"]/1e3) + 30, f"${row['total_spend']/1e3:.0f}K", ha="center", fontweight="bold", fontsize=9)
        axes[0, 0].text(i + w/2, (row["total_revenue"]/1e3) + 30, f"${row['total_revenue']/1e3:.0f}K", ha="center", fontweight="bold", fontsize=9)
        
    # 2. Conversions (Purchases)
    b_conv = axes[0, 1].bar(platform_df["ad_platform"], platform_df["purchases"], color=colors, edgecolor="black", linewidth=0.5)
    axes[0, 1].set_title("Total Conversions (Purchases)")
    axes[0, 1].set_ylabel("Purchases")
    for bar in b_conv:
        axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 25, f"{int(bar.get_height()):,}", ha="center", fontweight="bold")
    axes[0, 1].set_ylim(0, platform_df["purchases"].max() * 1.2)
    
    # 3. Cost Per Acquisition (CPA)
    b_cpa = axes[1, 0].bar(platform_df["ad_platform"], platform_df["cpa"], color=colors, edgecolor="black", linewidth=0.5)
    axes[1, 0].set_title("Cost Per Acquisition (CPA - Lower is Better)")
    axes[1, 0].set_ylabel("CPA ($)")
    for bar in b_cpa:
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f"${bar.get_height():.2f}", ha="center", fontweight="bold")
    axes[1, 0].set_ylim(0, platform_df["cpa"].max() * 1.2)
    
    # 4. Return on Ad Spend (ROAS)
    b_roas = axes[1, 1].bar(platform_df["ad_platform"], platform_df["roas"], color=colors, edgecolor="black", linewidth=0.5)
    axes[1, 1].set_title("Return On Ad Spend (ROAS - Higher is Better)")
    axes[1, 1].set_ylabel("ROAS (x)")
    axes[1, 1].axhline(1.0, color="gray", linestyle="--", label="Breakeven (1.0x)")
    for bar in b_roas:
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04, f"{bar.get_height():.2f}x", ha="center", fontweight="bold")
    axes[1, 1].set_ylim(0, platform_df["roas"].max() * 1.25)
    axes[1, 1].legend(loc="upper left")
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "platform_performance_comparison.png")
    plt.savefig(fig_path)
    plt.close()

def plot_campaign_performance(campaigns):
    """Plot 4: Top 10 vs Bottom 10 Campaigns by ROAS."""
    print("  -> Generating Figure 4: top_bottom_campaigns_roas.png ...")
    
    # Filter active campaigns with spend
    active_camps = campaigns[campaigns["total_spend"] > 0].copy()
    
    top_10 = active_camps.sort_values("roas", ascending=False).head(10)
    bottom_10 = active_camps.sort_values("roas", ascending=True).head(10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Top 10
    sns.barplot(data=top_10, y="campaign_name", x="roas", ax=ax1, palette="Greens_r", edgecolor="black", linewidth=0.5)
    ax1.set_title("Top 10 High-Performing Campaigns (by ROAS)")
    ax1.set_xlabel("ROAS Multiple (x)")
    ax1.set_ylabel("Campaign")
    ax1.axvline(1.0, color="red", linestyle="--", alpha=0.7, label="Breakeven (1.0x)")
    for p in ax1.patches:
        w = p.get_width()
        ax1.text(w + 0.03, p.get_y() + p.get_height()/2, f"{w:.2f}x", va="center", fontweight="bold", fontsize=9)
    ax1.legend()
    
    # Bottom 10
    sns.barplot(data=bottom_10, y="campaign_name", x="roas", ax=ax2, palette="Reds", edgecolor="black", linewidth=0.5)
    ax2.set_title("Lowest 10 Under-Performing Campaigns (by ROAS)")
    ax2.set_xlabel("ROAS Multiple (x)")
    ax2.set_ylabel("")
    ax2.axvline(1.0, color="red", linestyle="--", alpha=0.7, label="Breakeven (1.0x)")
    for p in ax2.patches:
        w = p.get_width()
        ax2.text(w + 0.03, p.get_y() + p.get_height()/2, f"{w:.2f}x", va="center", fontweight="bold", fontsize=9)
    ax2.legend()
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "top_bottom_campaigns_roas.png")
    plt.savefig(fig_path)
    plt.close()

def plot_ad_format_performance(ads):
    """Plot 5: Creative Format Performance (Video, Stories, Carousel, Image)."""
    print("  -> Generating Figure 5: ad_format_performance.png ...")
    
    format_df = ads.groupby("ad_type").agg(
        ads_count=("ad_id", "count"),
        total_spend=("ad_spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum"),
        revenue=("revenue", "sum")
    ).reset_index()
    
    format_df["ctr_percent"] = (format_df["clicks"] / format_df["impressions"]) * 100
    format_df["conversion_rate_percent"] = (format_df["purchases"] / format_df["clicks"]) * 100
    format_df["roas"] = format_df["revenue"] / format_df["total_spend"]
    format_df["cpa"] = format_df["total_spend"] / format_df["purchases"]
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    palette = sns.color_palette("deep", len(format_df))
    
    # 1. CTR by Format
    b1 = axes[0].bar(format_df["ad_type"], format_df["ctr_percent"], color=palette, edgecolor="black", linewidth=0.5)
    axes[0].set_title("Click-Through Rate (CTR %) by Format")
    axes[0].set_ylabel("CTR (%)")
    for bar in b1:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, f"{bar.get_height():.2f}%", ha="center", fontweight="bold")
    axes[0].set_ylim(0, format_df["ctr_percent"].max() * 1.2)
    
    # 2. Conversion Rate by Format
    b2 = axes[1].bar(format_df["ad_type"], format_df["conversion_rate_percent"], color=palette, edgecolor="black", linewidth=0.5)
    axes[1].set_title("Conversion Rate (CR %) by Format")
    axes[1].set_ylabel("Conversion Rate (%)")
    for bar in b2:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f"{bar.get_height():.2f}%", ha="center", fontweight="bold")
    axes[1].set_ylim(0, format_df["conversion_rate_percent"].max() * 1.2)
    
    # 3. ROAS by Format
    b3 = axes[2].bar(format_df["ad_type"], format_df["roas"], color=palette, edgecolor="black", linewidth=0.5)
    axes[2].set_title("Return On Ad Spend (ROAS) by Format")
    axes[2].set_ylabel("ROAS (x)")
    axes[2].axhline(1.0, color="gray", linestyle="--", label="Breakeven (1.0x)")
    for bar in b3:
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04, f"{bar.get_height():.2f}x", ha="center", fontweight="bold")
    axes[2].set_ylim(0, format_df["roas"].max() * 1.25)
    axes[2].legend()
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "ad_format_performance.png")
    plt.savefig(fig_path)
    plt.close()

def plot_audience_demographics(ads, users, events):
    """Plot 6: Audience Performance by Age Group and Gender."""
    print("  -> Generating Figure 6: audience_demographics_analysis.png ...")
    
    # Target Age Group from ads
    age_perf = ads.groupby("target_age_group").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum"),
        spend=("ad_spend", "sum"),
        revenue=("revenue", "sum")
    ).reset_index()
    age_perf["roas"] = age_perf["revenue"] / age_perf["spend"]
    age_perf["ctr_percent"] = (age_perf["clicks"] / age_perf["impressions"]) * 100
    
    # Target Gender from ads
    gender_perf = ads.groupby("target_gender").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        purchases=("purchases", "sum"),
        spend=("ad_spend", "sum"),
        revenue=("revenue", "sum")
    ).reset_index()
    gender_perf["roas"] = gender_perf["revenue"] / gender_perf["spend"]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Age Group Performance
    sns.barplot(data=age_perf, x="target_age_group", y="roas", ax=ax1, palette="crest", edgecolor="black", linewidth=0.5)
    ax1.set_title("ROAS by Target Age Group")
    ax1.set_xlabel("Target Age Group")
    ax1.set_ylabel("ROAS (x)")
    ax1.axhline(1.0, color="red", linestyle="--", label="Breakeven (1.0x)")
    for p in ax1.patches:
        h = p.get_height()
        ax1.text(p.get_x() + p.get_width()/2, h + 0.03, f"{h:.2f}x", ha="center", fontweight="bold")
    ax1.set_ylim(0, age_perf["roas"].max() * 1.25)
    ax1.legend()
    
    # Gender Performance Donut / Bar
    colors = ["#4FC3F7", "#F06292", "#BA68C8"]
    wedges, texts, autotexts = ax2.pie(
        gender_perf["purchases"],
        labels=gender_perf["target_gender"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="black", linewidth=0.8),
        textprops=dict(fontweight="bold")
    )
    ax2.set_title("Share of Purchases by Target Gender")
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, "audience_demographics_analysis.png")
    plt.savefig(fig_path)
    plt.close()

def main():
    print("="*70)
    print("PHASE 4: EXECUTING EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*70)
    
    campaigns, ads, daily, users, events = load_data()
    
    plot_conversion_funnel(events)
    plot_monthly_trends(daily)
    plot_platform_comparison(ads)
    plot_campaign_performance(campaigns)
    plot_ad_format_performance(ads)
    plot_audience_demographics(ads, users, events)
    
    print("\n" + "="*70)
    print(f"ALL 6 VISUALIZATION FIGURES EXPORTED TO: {FIGURES_DIR}")
    print("="*70)

if __name__ == "__main__":
    main()
