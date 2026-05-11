# Databricks notebook source
# MAGIC %md
# MAGIC **Data Cleaning** 
# MAGIC
# MAGIC Here we will:
# MAGIC - trim spaces
# MAGIC - remove duplicates
# MAGIC - standardize categories
# MAGIC - remove -ve and commas from numeric values
# MAGIC - standardize date formats

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW sales_insurance_project_raw_dataset USING csv
# MAGIC OPTIONS (path "/Volumes/workspace/dataforge26/salesdata/dfa_insurance_project_raw_dataset.csv", header "true", inferSchema "true")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_insurance_project_raw_dataset
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW insurance_project_stage AS
# MAGIC SELECT
# MAGIC  TRIM (Policy_ID) As Policy_ID,
# MAGIC  TRIM (Claim_ID) AS Claim_ID,
# MAGIC  CAST(TRIM(Age) AS INT) AS Age,  --There are no Nulls in Age as per Exploration Notebook, and already numeric
# MAGIC
# MAGIC   CASE 
# MAGIC     WHEN TRIM(Customer_ID) = '' THEN "Unknown Customer" --There are 3 unkown customers, their data seems to be correct but it was probably a a data capturing error
# MAGIC     ELSE TRIM(Customer_ID)
# MAGIC   END AS Customer_ID,
# MAGIC
# MAGIC   CASE 
# MAGIC     WHEN TRIM(Gender) = '' THEN 'Unknown'
# MAGIC     WHEN UPPER(TRIM(Gender)) IN ('MALE', 'M')
# MAGIC     THEN 'Male'
# MAGIC     WHEN UPPER(TRIM(Gender)) IN ('FEMALE', 'F')
# MAGIC     THEN 'Female'
# MAGIC     ELSE TRIM(Gender)
# MAGIC   END AS Gender,
# MAGIC
# MAGIC   CASE
# MAGIC     WHEN Province IS NULL OR TRIM(Province) = '' THEN 'Unknown'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('western cape', 'wc') THEN 'Western Cape'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('eastern cape', 'ec') THEN 'Eastern Cape'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('free state', 'fs') THEN 'Free State'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('gauteng', 'gp') THEN 'Gauteng'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('kwazulu-natal', 'kwazulu natal', 'kzn') THEN 'KwaZulu-Natal'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('limpopo', 'lp') THEN 'Limpopo'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('mpumalanga', 'mp') THEN 'Mpumalanga'
# MAGIC     WHEN LOWER(TRIM(Province)) IN ('north west', 'nw') THEN 'North West'
# MAGIC     ELSE INITCAP(TRIM(Province))
# MAGIC   END AS Province,
# MAGIC
# MAGIC   CASE
# MAGIC     WHEN Policy_Type IS NULL OR TRIM(Policy_Type) = '' THEN 'Unknown'
# MAGIC     ELSE INITCAP(TRIM(Policy_Type))
# MAGIC   END AS Policy_Type,
# MAGIC
# MAGIC   CASE 
# MAGIC     WHEN Policy_Status IS NULL OR TRIM (Policy_Status) = '' THEN 'Unknown'
# MAGIC     ELSE INITCAP(TRIM(Policy_Status))
# MAGIC   END AS Policy_Status,
# MAGIC
# MAGIC   CASE 
# MAGIC    WHEN Claim_Status IS NULL OR TRIM (Claim_Status) = '' THEN 'Unknown'
# MAGIC    ELSE INITCAP(TRIM(Claim_Status))
# MAGIC   END AS Claim_Status,
# MAGIC
# MAGIC   DATE_FORMAT(
# MAGIC   CASE
# MAGIC     WHEN Claim_Date RLIKE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
# MAGIC       THEN TO_DATE(Claim_Date, 'yyyy-MM-dd')
# MAGIC       
# MAGIC     WHEN Claim_Date RLIKE '^[0-9]{4}/[0-9]{2}/[0-9]{2}$'
# MAGIC       THEN TO_DATE(Claim_Date, 'yyyy/MM/dd')
# MAGIC       
# MAGIC     WHEN Claim_Date RLIKE '^[0-9]{2}-[A-Za-z]{3}-[0-9]{4}$'
# MAGIC       THEN TO_DATE(Claim_Date, 'dd-MMM-yyyy')
# MAGIC       
# MAGIC     ELSE NULL
# MAGIC   END,
# MAGIC   'yyyy-MM-dd'
# MAGIC   ) AS Claim_Date,
# MAGIC
# MAGIC     DATE_FORMAT(
# MAGIC   CASE
# MAGIC     WHEN Join_Date RLIKE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
# MAGIC       THEN TO_DATE(Join_Date, 'yyyy-MM-dd')
# MAGIC       
# MAGIC     WHEN Join_Date RLIKE '^[0-9]{4}/[0-9]{2}/[0-9]{2}$'
# MAGIC       THEN TO_DATE(Join_Date, 'yyyy/MM/dd')
# MAGIC       
# MAGIC     WHEN Join_Date RLIKE '^[0-9]{2}-[A-Za-z]{3}-[0-9]{4}$'   ---converting when date has month as 3 letter abbreviation
# MAGIC       THEN TO_DATE(Join_Date, 'dd-MMM-yyyy')
# MAGIC       
# MAGIC     ELSE NULL
# MAGIC   END,
# MAGIC   'yyyy-MM-dd'  ---final formating of date as yyyy - MM - dd
# MAGIC   ) AS Join_Date, 
# MAGIC
# MAGIC  CAST(
# MAGIC     NULLIF(
# MAGIC       REPLACE(REPLACE(TRIM(Claim_Amount), ',', ''), 'R', ''), --converting Claim_Amount to numeric considering R as well as comma as decimal separator
# MAGIC       ''
# MAGIC     ) AS DECIMAL(18,2)
# MAGIC   ) AS Claim_Amount, 
# MAGIC
# MAGIC   CAST(
# MAGIC     NULLIF(
# MAGIC       REPLACE(REPLACE(TRIM(Monthly_Income), ',', ''), 'R', ''), --converting Monthyly_Income
# MAGIC       ''
# MAGIC     ) AS DECIMAL(18,2)
# MAGIC   ) AS Monthly_Income, 
# MAGIC
# MAGIC   CAST(
# MAGIC     NULLIF(
# MAGIC       REPLACE(REPLACE(TRIM(Premium_Amount), ',', ''), 'R', ''), --converting Premium_Amount
# MAGIC       ''
# MAGIC     ) AS DECIMAL(18,2)
# MAGIC   ) AS Premium_Amount, 
# MAGIC
# MAGIC   CASE
# MAGIC     WHEN LOWER(TRIM(Fraud_Flag)) IN ('yes', 'y', '1') THEN 'Yes' --Fraud_flag can be yes/no or 1/0 or missing according to Exploration Notebook
# MAGIC     WHEN LOWER(TRIM(Fraud_Flag)) IN ('no', 'n', '0') THEN 'No'
# MAGIC     ELSE 'Unknown'
# MAGIC   END AS Fraud_Flag
# MAGIC FROM sales_insurance_project_raw_dataset; 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking what the dataset now looks like 
# MAGIC SELECT * FROM insurance_project_stage
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql 
# MAGIC --- Checking for null and invalid data ---
# MAGIC SELECT
# MAGIC     SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS Null_Age, 
# MAGIC     SUM(CASE WHEN Age < 18 OR Age > 100 THEN 1 ELSE 0 END) AS Invalid_Age,
# MAGIC     SUM(CASE WHEN Customer_ID = "Unknown Customer" THEN 1 ELSE 0 END) AS Null_Customer_ID,
# MAGIC     SUM (CASE WHEN Premium_Amount Is NULL THEN 1 ELSE 0 END) AS Null_Premium_Amount,
# MAGIC     SUM (CASE WHEN Premium_Amount < 0 THEN 1 ELSE 0 END) AS Negative_Premium_Amount,
# MAGIC     SUM (CASE WHEN Monthly_Income Is NULL THEN 1 ELSE 0 END) AS Null_Monthly_Income,
# MAGIC     SUM (CASE WHEN Monthly_Income < 0 THEN 1 ELSE 0 END) AS Negative_Monthly_Income,
# MAGIC     SUM (CASE WHEN Claim_Amount Is NULL THEN 1 ELSE 0 END) AS Null_Claim_Amount,
# MAGIC     SUM (CASE WHEN Claim_Amount < 0 THEN 1 ELSE 0 END) AS Negative_Claim_Amount
# MAGIC FROM insurance_project_stage;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Province check ---
# MAGIC SELECT Province, COUNT(*) AS cnt
# MAGIC FROM insurance_project_stage
# MAGIC GROUP BY Province
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- checking when Customer ID is "unknown"
# MAGIC SELECT *
# MAGIC FROM insurance_project_clean
# MAGIC WHERE Customer_ID = 'Unknown Customer'

# COMMAND ----------

# MAGIC %sql
# MAGIC /* Removing of duplicates and bad rows which includes
# MAGIC - Keeping first exact duplicates
# MAGIC - Keeping ages between 18 - 100 as these are insurance rules
# MAGIC - Removing rows with negative claim amount, monthly income and premium amount*/
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW insurance_project_clean AS
# MAGIC WITH DEDUPED AS (
# MAGIC   SELECT *,
# MAGIC     ROW_NUMBER() OVER
# MAGIC     (PARTITION BY 
# MAGIC     Customer_ID, Policy_ID, Age, Gender, Province, Policy_Type, Policy_Status, Claim_Status, Claim_ID, Claim_Date, Join_Date, Claim_Amount, Monthly_Income, Premium_Amount, Fraud_Flag
# MAGIC     ORDER BY Policy_ID ASC) AS rn
# MAGIC   FROM insurance_project_stage
# MAGIC )
# MAGIC SELECT *
# MAGIC FROM DEDUPED
# MAGIC   WHERE rn = 1
# MAGIC   AND Age BETWEEN 18 AND 100
# MAGIC   AND Claim_Amount >= 0
# MAGIC   AND Premium_Amount >=0
# MAGIC   AND Monthly_Income >=0 ; 
# MAGIC
# MAGIC SELECT * FROM insurance_project_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC --Clean check of data now --
# MAGIC SELECT * FROM insurance_project_clean
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Checking table --
# MAGIC DESCRIBE TABLE insurance_project_clean; 

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking for null and invalid data after removing bad rows---
# MAGIC SELECT
# MAGIC     SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS Null_Age, 
# MAGIC     SUM(CASE WHEN Age < 18 OR Age > 100 THEN 1 ELSE 0 END) AS Invalid_Age,
# MAGIC     SUM(CASE WHEN Customer_ID = "Unknown Customer" THEN 1 ELSE 0 END) AS Null_Customer_ID,
# MAGIC     SUM (CASE WHEN Premium_Amount Is NULL THEN 1 ELSE 0 END) AS Null_Premium_Amount,
# MAGIC     SUM (CASE WHEN Premium_Amount < 0 THEN 1 ELSE 0 END) AS Negative_Premium_Amount,
# MAGIC     SUM (CASE WHEN Monthly_Income Is NULL THEN 1 ELSE 0 END) AS Null_Monthly_Income,
# MAGIC     SUM (CASE WHEN Monthly_Income < 0 THEN 1 ELSE 0 END) AS Negative_Monthly_Income,
# MAGIC     SUM (CASE WHEN Claim_Amount Is NULL THEN 1 ELSE 0 END) AS Null_Claim_Amount,
# MAGIC     SUM (CASE WHEN Claim_Amount < 0 THEN 1 ELSE 0 END) AS Negative_Claim_Amount
# MAGIC FROM insurance_project_clean;

# COMMAND ----------

# MAGIC %sql
# MAGIC --Total claim amount
# MAGIC SELECT SUM(Claim_Amount) AS Total_Claim_Amount
# MAGIC FROM insurance_project_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Number of customers ---
# MAGIC SELECT COUNT(DISTINCT Customer_ID) AS Num_Customers
# MAGIC FROM insurance_project_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Number of policies ---
# MAGIC SELECT COUNT(DISTINCT Policy_ID) AS Num_Policies
# MAGIC FROM insurance_project_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Number of Claims by policy type
# MAGIC SELECT Policy_Type, COUNT(*) AS Claim_Count
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY Policy_Type
# MAGIC ORDER BY Claim_Count

# COMMAND ----------

# MAGIC %sql
# MAGIC --Total number of policies--
# MAGIC SELECT COUNT(*) AS Num_Policies
# MAGIC FROM insurance_project_clean

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Total number of claims (by Type)
# MAGIC SELECT 
# MAGIC   Claim_Status,
# MAGIC   COUNT(*) AS total_claims
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY Claim_Status
# MAGIC ORDER BY total_claims DESC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC --Average claim amount per policy type--
# MAGIC SELECT Policy_Type, ROUND(AVG(Claim_Amount), 2) AS Avg_Claim_Amount
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY Policy_Type
# MAGIC ORDER BY Avg_Claim_Amount DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Number of fraud vs non-fraud claims
# MAGIC SELECT 
# MAGIC   Fraud_Flag,
# MAGIC   COUNT(*) AS num_claims
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY Fraud_Flag
# MAGIC ORDER BY num_claims DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC --Top 5 highest claim amounts
# MAGIC SELECT Claim_ID, Policy_ID, Claim_Amount
# MAGIC FROM insurance_project_clean
# MAGIC ORDER BY Claim_Amount DESC
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Claims per location (Number of claims and total claim amount)
# MAGIC SELECT Province, COUNT(*) AS Claim_Count, SUM(Claim_Amount) AS Total_Claim_Amount
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY Province
# MAGIC ORDER BY Claim_Count DESC

# COMMAND ----------

# DBTITLE 1,Cell 21
# MAGIC %sql
# MAGIC -- Claims trend over time
# MAGIC SELECT 
# MAGIC   DATE_FORMAT(TO_DATE(Claim_Date, 'yyyy-MM-dd'), 'yyyy-MM') AS claim_month,
# MAGIC   COUNT(*) AS num_claims
# MAGIC FROM insurance_project_clean
# MAGIC GROUP BY DATE_FORMAT(TO_DATE(Claim_Date, 'yyyy-MM-dd'), 'yyyy-MM')
# MAGIC ORDER BY claim_month;