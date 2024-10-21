# Databricks notebook source
# emp - dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/emp.parquet
# dep - dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/dep.parquet
# emp - dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/emp1.csv
# dep - dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/dep1.csv

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
import dlt

# COMMAND ----------

@dlt.table(
  comment="Employee Delta Live Table",
)
def emp_table():
  return (
    #spark.read.parquet('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/emp.parquet')
    spark.read.csv('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/emp1.csv',header=True,inferSchema=True)
  )

# COMMAND ----------

@dlt.table(
  comment="Department Delta Live Table",
)
def dep_table():
  return (
    # spark.read.parquet('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/dep.parquet')
    spark.read.csv('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/dep1.csv',header=True,inferSchema=True)
  )

# COMMAND ----------

@dlt.table(
  comment="Transformed Table with Employee and Department",
)

def emp_dep_table():
  empDF = spark.read.csv('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/emp1.csv',header=True,inferSchema=True)
  depDF = spark.read.csv('dbfs:/FileStore/shared_uploads/iriscloudone@outlook.com/dep1.csv',header=True,inferSchema=True)
  emp_with_dep_joinedDF = empDF.join(depDF,'department_id')

  emp_with_dep_joinedDF.write.format('delta').save(
    '/empdeptable',mode='overwrite'
  )

  return (
    spark.read.format('delta').load('/empdeptable')
  )


# COMMAND ----------

@dlt.table(
  comment="Max Salary Query by Dep",
)
def max_salary_by_dep():
  
  max_salary_by_depQuery = spark.sql('SELECT max(salary) as MaxSalary,department_name FROM emp_dep_table GROUP BY department_name')

  return max_salary_by_depQuery

# COMMAND ----------

@dlt.table(
    comment="Avg Salary by Department",
    table_properties={"myCompanyPipeline.quality": "Gold"},
)
def outcome():
    result = dlt.read("max_salary_by_dep")
    return result

outcome()


# COMMAND ----------

outcome()

# COMMAND ----------

display(spark.sql('SELECT * FROM live.max_salary_by_dep'))

# COMMAND ----------

display(spark.sql('SELECT * FROM default.empdeptable'))

# COMMAND ----------

display(spark.sql('SELECT * FROM live.max_salary_by_dep'))
