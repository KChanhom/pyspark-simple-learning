from __future__ import annotations

from pyspark.sql import functions as sql_func

from src.config import OUTPUT_DIR, RAW_DIR
from src.spark_session import get_spark


def main() -> None:
    spark = get_spark("wordcount")

    input_path = RAW_DIR / "text.txt"
    output_path = OUTPUT_DIR / "wordcount"

    # Read text file input to DataFrame
    lines = spark.read.text(str(input_path))

    words = (
        lines
        .select(sql_func.col("value").alias("line"))
        .withColumn("line_lower", sql_func.lower(sql_func.col("line")))
        .withColumn("word", sql_func.explode(sql_func.split(sql_func.col("line_lower"), r"\W+")))
        .filter(sql_func.length(sql_func.col("word")) > 0)
        .select(sql_func.col("word"))
    )

    counts = words.groupBy("word").count().orderBy(sql_func.desc("count"), sql_func.asc("word"))
    counts.show(30, truncate=False)

    # เขียนเป็น CSV เพื่อเปิดดูง่าย (coalesce(1) เพื่อให้ได้ไฟล์เดียว)
    (
        counts.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(output_path))
    )

    spark.stop()


if __name__ == "__main__":
    # ช่วยให้ `python -m src.jobs.wordcount` ทำงานได้
    main()

