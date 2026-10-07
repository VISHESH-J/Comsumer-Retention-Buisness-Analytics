# E-Commerce Revenue & Customer Analytics

## Overview

This project analyzes the Olist Brazilian e-commerce dataset to understand sales performance, customer behavior, product performance, delivery operations, and customer satisfaction.

The project uses Python and pandas to transform raw e-commerce data into actionable business insights.

## Objectives

The analysis focuses on:

- Sales and order performance
- Customer retention and repeat purchasing
- RFM customer segmentation
- Product and category performance
- Delivery performance
- Customer review behavior
- Business opportunities and recommendations

## Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset.

The dataset contains information about:

- Orders
- Customers
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translations

## Project Workflow

Raw Data
↓
Data Profiling
↓
Data Cleaning
↓
Data Validation
↓
Analytical Data Preparation
↓
Business Analysis
↓
Customer Segmentation
↓
Product & Category Analysis
↓
Delivery & Review Analysis
↓
Business Insights
↓
Recommendations

## Tools & Technologies

- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- Git / GitHub

## Notebook Structure

### 01_data_profiling.ipynb
Explores the structure, columns, data types, missing values, and basic characteristics of the source datasets.

### 02_data_cleaning.ipynb
Performs data type standardization, timestamp conversion, text/ID cleaning, and creates cleaned datasets.

### 03_data_analysis.ipynb
Performs the main analytical work including:

- Sales analysis
- Customer analysis
- Repeat purchase analysis
- RFM segmentation
- Cohort analysis
- Product and category analysis
- Delivery analysis
- Review analysis
- Business opportunity analysis

### 04_business_insights.ipynb
Presents the final business-focused analysis, key insights, opportunities, recommendations, and conclusions.

## Key Analytical Concepts

### RFM Analysis

Customers are segmented using:

- Recency
- Frequency
- Monetary Value

This identifies customer groups such as:

- High Value
- Loyal / Active
- Potential Loyalist
- At Risk
- High Value At Risk
- Other

### Delivery Analysis

Delivery performance is evaluated using:

- Delivery duration
- Delivery delay
- On-time vs late delivery
- Relationship between delivery performance and review scores

## Business Value

The analysis helps identify opportunities related to:

- Customer retention
- High-value customer loyalty
- Repeat purchasing
- Delivery performance
- Category optimization
- Customer satisfaction

## Project Structure

```text
CBA PROJECT/
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebook/
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_analysis.ipynb
│   └── 04_business_insights.ipynb
│
└── README.md
