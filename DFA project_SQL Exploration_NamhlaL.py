# Databricks notebook source
# MAGIC %md
# MAGIC **Data Exploration notebook**
# MAGIC
# MAGIC _Here we review each column to understand what steps we need to take to clean the data_

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Customer Risk & Claims Analysis for an Insurance Company ---
# MAGIC SELECT* 
# MAGIC from csv. `/Volumes/workspace/dataforge26/salesdata/dfa_insurance_project_raw_dataset.csv`
# MAGIC LIMIT 20

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW sales_insurance_project_raw_dataset USING csv
# MAGIC OPTIONS (path "/Volumes/workspace/dataforge26/salesdata/dfa_insurance_project_raw_dataset.csv", header "true", inferSchema "true")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_insurance_project_raw_dataset
# MAGIC LIMIT 20; 

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking Customer_ID Column --
# MAGIC SELECT Customer_ID, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Customer_ID
# MAGIC ORDER BY cnt DESC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Checking the unknown customers ---
# MAGIC SELECT *
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC WHERE Customer_ID = ' ';

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Total Number of distinct customers ---
# MAGIC SELECT 
# MAGIC  COUNT (Customer_ID) AS total_records,
# MAGIC  COUNT(DISTINCT Customer_ID) AS total_unique_customers
# MAGIC FROM sales_insurance_project_raw_dataset

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Total number of policies ---
# MAGIC SELECT 
# MAGIC  COUNT (Policy_ID) AS total_records,
# MAGIC  COUNT(DISTINCT Policy_ID) AS total_unique_policies
# MAGIC FROM sales_insurance_project_raw_dataset

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking Policy Type ---
# MAGIC SELECT Policy_Type, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Policy_Type
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Checking Claim Status ---
# MAGIC SELECT Claim_Status, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Claim_Status
# MAGIC ORDER BY cnt DESC
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC ---Total claim amount ---
# MAGIC --Check claim_amount column
# MAGIC SELECT Claim_Amount, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC Group by Claim_Amount
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Checking region ---
# MAGIC SELECT Province, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Province
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC ---checking gender ---
# MAGIC SELECT Gender, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Gender
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC ---Checking age ---
# MAGIC SELECT Age, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Age
# MAGIC ORDER BY cnt

# COMMAND ----------

# MAGIC %sql
# MAGIC --Checking dates --
# MAGIC SELECT Claim_Date, Join_Date
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC LIMIT 50

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking Fraud_flag ---
# MAGIC SELECT Fraud_Flag, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Fraud_Flag
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC --- Checking Policy_Status ---
# MAGIC SELECT Policy_Status, COUNT(*) AS cnt
# MAGIC FROM sales_insurance_project_raw_dataset
# MAGIC GROUP BY Policy_Status
# MAGIC ORDER BY cnt DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC ---checking null or blank values--
# MAGIC SELECT
# MAGIC   SUM(CASE WHEN Customer_ID is NULL OR TRIM(Customer_ID) = '' THEN 1 ELSE 0 END) AS missing_customerid,
# MAGIC   SUM(CASE WHEN Policy_ID is NULL OR TRIM(Policy_ID) = '' THEN 1 ELSE 0 END) AS missing_policy_id,
# MAGIC   SUM(CASE WHEN Policy_Type is NULL OR TRIM(Policy_Type) = '' THEN 1 ELSE 0 END) AS missing_policy_type,
# MAGIC   SUM(CASE WHEN Claim_Status is NULL OR TRIM(Claim_Status) = '' THEN 1 ELSE 0 END) AS missing_claim_status,
# MAGIC   SUM(CASE WHEN Claim_Amount is NULL OR TRIM(Claim_Amount) = '' THEN 1 ELSE 0 END) AS missing_claim_amount,
# MAGIC   SUM(CASE WHEN Premium_Amount is NULL OR TRIM(Premium_Amount) = '' THEN 1 ELSE 0 END) AS missing_premium_amount,
# MAGIC   SUM(CASE WHEN Fraud_Flag is NULL OR TRIM(Fraud_Flag) = '' THEN 1 ELSE 0 END) AS missing_fraud_flag, 
# MAGIC   SUM(CASE WHEN Province is NULL OR TRIM(Province) = '' THEN 1 ELSE 0 END) AS missing_province,
# MAGIC   SUM(CASE WHEN Gender is NULL OR TRIM(Gender) = '' THEN 1 ELSE 0 END) AS missing_gender, 
# MAGIC   SUM(CASE WHEN Age is NULL OR TRIM(Age) = '' THEN 1 ELSE 0 END) AS missing_Age
# MAGIC FROM sales_insurance_project_raw_dataset