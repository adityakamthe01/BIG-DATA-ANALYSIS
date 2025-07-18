# -*- coding: utf-8 -*-
"""Aditya Kamathe Task 1 Big data Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a1qoDoHtseItie6O90o1X43kTo-l-Igo
"""

pip install pyspark

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("InstagramAnalysis").getOrCreate()

df = spark.read.csv("/content/drive/MyDrive/task data set/Instagram data.csv", header=True, inferSchema=True)
df.printSchema()
df.show(5)

# Show summary statistics
df.describe().show()

# Count of nulls per column
from pyspark.sql.functions import col, isnan, when, count

df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

df.orderBy(df.Likes.desc()).select("Caption", "Likes", "Impressions").show(5, truncate=False)

from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler

vec_assembler = VectorAssembler(inputCols=["Likes", "Follows"], outputCol="features")
df_vector = vec_assembler.transform(df).select("features")

correlation = Correlation.corr(df_vector, "features").head()[0]
print(f"Correlation Matrix:\n{correlation}")

df.select("Impressions", "Likes", "Shares", "Follows", "Profile Visits").groupBy().avg().show()

from pyspark.sql.functions import explode, split, lower, trim

hashtags_split = df.withColumn("Hashtag", explode(split(col("Hashtags"), "#")))
hashtags_clean = hashtags_split.withColumn("Hashtag", trim(lower(col("Hashtag"))))
hashtags_clean.groupBy("Hashtag").count().orderBy("count", ascending=False).show(10, truncate=False)

df_summary = df.select("Caption", "Likes", "Impressions")
df_summary.write.csv("insights_output", header=True)