# Business Requirements Document

## Project Title

**The Rising Cost of Living in Portugal: An Analysis of Consumer Price Inflation**

---

## 1. Project Overview

### Motivation

Over recent years, consumers in Portugal have experienced significant changes in the prices of goods and services. However, the headline inflation rate provides only a broad overview of price changes and does not reveal which categories are driving these increases.

This project aims to investigate how consumer prices in Portugal have evolved in recent years and identify the main categories contributing to inflation and the rising cost of living.

### Objective

The primary objective of this project is to analyse the evolution of consumer prices in Portugal from 2019 to 2026 and identify the categories that have contributed most significantly to price increases during this period.

The analysis will pay particular attention to the period from 2023 onwards, investigating whether inflationary pressures and price increases during this period have been greater than those observed in previous years.

### Scope

The analysis will focus on Portugal and will use monthly data from Eurostat.

The primary period of analysis will be January 2019 to the latest complete month available in 2026.

The analysis will focus on:

- Overall consumer price inflation;
- Food prices;
- Energy prices;
- Prices of goods and services;
- Housing-related costs, including rents and house prices, where suitable data are available;
- Changes in these categories over time.

The project will initially focus on Portugal and will not include international comparisons.

---

## 2. Data and Key Definitions

### Harmonised Index of Consumer Prices (HICP)

The **Harmonised Index of Consumer Prices (HICP)** is an index developed by Eurostat to measure changes over time in the prices of goods and services consumed by households.

It provides a harmonised methodology that allows consumer price inflation to be measured consistently across European countries.

The HICP is based on a basket of goods and services representing household consumption. The basket is divided into different categories, such as food, energy, transport, housing-related goods and services, restaurants and hotels, and other consumer goods and services.

In this project, HICP data will be used as the primary measure of consumer price inflation.

It is important to note that HICP measures **changes in consumer prices**, rather than directly measuring an individual's personal cost of living or purchasing power.

---

## 3. Analytical Approach

The project will primarily use **descriptive and exploratory data analysis (EDA)**.

The analysis will seek to answer:

- How have consumer prices in Portugal evolved since 2019?
- When were the largest increases in consumer prices observed?
- Which categories experienced the greatest price increases?
- Which categories contributed most to periods of high inflation?
- How did food and energy prices evolve relative to overall inflation?
- How have housing-related costs, including rents and house prices, evolved during the same period?
- Did the composition of price increases change between the earlier and later periods of the analysis?

The analysis will focus on identifying patterns, trends, changes over time and relationships between categories rather than predicting future inflation or establishing causal relationships.

---

## 4. Hypotheses

### H1: Inflationary pressure increased significantly from 2023 onwards.

Consumer price inflation in Portugal was higher and/or more persistent during the 2023–2026 period than during the earlier years of the analysis.

### H2: Food, energy and housing-related costs were major contributors to the increase in the cost of living.

Food and energy prices are expected to have played an important role in the increase in consumer prices, while housing-related costs, particularly rents and house purchase prices, may have increased substantially during the same period.

This hypothesis will be investigated using HICP data alongside appropriate Eurostat housing and rent price indicators.

### H3: Different categories experienced substantially different price trajectories.

The overall inflation rate is expected to mask significant differences between categories of goods and services. Some categories are expected to have experienced considerably larger and/or more persistent price increases than others.

---

## 5. Success Factors

The project will be considered successful if it:

- Clearly describes the evolution of consumer prices in Portugal since 2019;
- Identifies the periods of greatest inflationary pressure;
- Identifies the categories with the largest price increases;
- Evaluates the three proposed hypotheses using appropriate data;
- Clearly distinguishes between overall inflation and changes in specific categories;
- Produces clear and informative visualisations;
- Provides evidence-based insights rather than merely describing charts;
- Documents the data sources, methodology and analytical decisions clearly enough for the analysis to be reproduced.

---

## 6. Assumptions and Constraints

### Assumptions

- HICP is an appropriate and consistent measure for analysing consumer price inflation in Portugal.
- Eurostat data provide sufficiently reliable and consistent measurements for the period under analysis.
- The categories included in the analysis are sufficiently representative to investigate the main drivers of consumer price changes.

### Constraints

- The analysis is limited to publicly available Eurostat data.
- HICP measures price changes in a standardised consumption basket and does not represent the individual spending patterns of every household.
- Housing costs, particularly house purchase prices, are not fully captured by HICP and will therefore require complementary datasets.
- The analysis will identify patterns and associations but will not establish causal relationships.
- The project will initially focus exclusively on Portugal.

---

## 7. Requirements

To achieve the project objectives, the following requirements must be fulfilled:

1. Obtain the relevant data programmatically through the Eurostat API.
2. Identify and document the relevant Eurostat datasets and variables.
3. Clean and transform the data using Python and Pandas.
4. Analyse monthly and annual changes in consumer prices.
5. Analyse the evolution of the main HICP categories.
6. Investigate food and energy price changes.
7. Investigate housing-related indicators, including rents and house prices, using complementary Eurostat datasets where appropriate.
8. Test the proposed hypotheses using descriptive and exploratory analysis.
9. Create appropriate data visualisations to communicate the findings.
10. Document the methodology, findings and limitations.
11. Produce a reproducible Jupyter Notebook suitable for publication as a portfolio project on GitHub.

---

## 8. Expected Deliverables

The project will produce:

- A reproducible Python/Jupyter Notebook;
- Cleaned and transformed datasets;
- Exploratory data analysis;
- Data visualisations;
- A summary of key findings;
- An evaluation of the three hypotheses;
- Documentation of data sources and methodology;
- A GitHub repository containing the complete project.

---

## 9. Glossary

**HICP (Harmonised Index of Consumer Prices):**  
A Eurostat index measuring changes over time in the prices of goods and services consumed by households, using a harmonised methodology across European countries.

**Inflation rate:**  
The percentage change in the general level of consumer prices over a specified period.

**Consumer prices:**  
Prices paid by households for goods and services included in the consumption basket.

**HICP category:**  
A group of goods and/or services classified according to the European Classification of Individual Consumption According to Purpose (ECOICOP).

**Price index:**  
A statistical measure used to track changes in the prices of a defined basket of goods and services over time.

**Cost of living:**  
The amount of money required to maintain a particular standard of living. In this project, changes in consumer prices are used as an indicator of changing costs faced by households, but HICP should not be interpreted as a complete measure of individual household cost of living.

**Monthly Year-on-Year Inflation Rate:**  
The percentage change in prices in a given month compared with the same month of the previous year. For example, the monthly year-on-year inflation rate for March 2025 compares prices in March 2025 with prices in March 2024. This is the measure used in the HICP monthly annual rate of change dataset.

**Quarterly Inflation Rate:**  
The percentage change in prices over a quarter. Unless otherwise specified, it commonly refers to the change from one quarter to the previous quarter. For example, a quarterly inflation rate for 2025-Q1 compares prices in 2025-Q1 with prices in 2024-Q4.

**Quarterly Year-on-Year Inflation Rate:**  
The percentage change in prices in a given quarter compared with the same quarter of the previous year. For example, the quarterly year-on-year inflation rate for 2025-Q1 compares average prices in 2025-Q1 with average prices in 2024-Q1.

**Mean Monthly Year-on-Year Inflation Rate:**  
A quarterly summary calculated as the arithmetic mean of the three monthly year-on-year inflation rates within a calendar quarter. In this project, it is used to align the monthly HICP data with the quarterly House Price Index dataset. It is not an official quarterly inflation rate and should be interpreted as an average measure of inflationary pressure during that quarter.

**Year-on-Year Rate of Change (Annual Rate of Change):**  
The percentage change in the value of an indicator compared with the same period of the previous year. For monthly data, a year-on-year rate compares a given month with the same month one year earlier. For example, a year-on-year inflation rate of 3% in March 2025 indicates that prices were, on average, 3% higher than in March 2024. In Portuguese, this is commonly referred to as a *taxa de variação homóloga*.