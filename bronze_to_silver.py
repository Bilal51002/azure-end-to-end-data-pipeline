# Databricks notebook source
dbutils.library.restartPython() 

# COMMAND ----------

# Databricks notebook source
# MAGIC %md
# MAGIC # Single table column transformation
# MAGIC

# COMMAND ----------

dbutils.fs.ls('abfss://bronze@intechsg202608.dfs.core.windows.net/SalesLT/')

# COMMAND ----------

dbutils.fs.ls('abfss://silver@intechsg202608.dfs.core.windows.net/')

# COMMAND ----------

df = spark.read.format('parquet').load('abfss://bronze@intechsg202608.dfs.core.windows.net/SalesLT/Address/Address.parquet')

# COMMAND ----------

display(df)

# COMMAND ----------

len(df.columns)
df.count()

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

df = df.withColumn("ModifiedDate", date_format(from_utc_timestamp(df['ModifiedDate'].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT 1 as colum1

# COMMAND ----------

# MAGIC %md
# MAGIC # Date transformation for tables

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls('abfss://bronze@intechsg202608.dfs.core.windows.net/SalesLT/'):
    table_name.append(i.name.split('/')[0])

table_name

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

for i in table_name:
    path = 'abfss://bronze@intechsg202608.dfs.core.windows.net/SalesLT/' + i + '/' + i + '.parquet'
    df = spark.read.format('parquet').load(path)
    column = df.columns

    for col in column:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))
    
    output_path = 'abfss://silver@intechsg202608.dfs.core.windows.net/SalesLT/' + i + '/'
    df.write.format('delta').mode('overwrite').save(output_path)

# COMMAND ----------

display(df)