from __future__ import annotations

from pyspark.sql import functions as sql_func

from src.config import OUTPUT_DIR, RAW_DIR
from src.spark_session import get_spark


def main() -> None:
    spark = get_spark("etl_users_orders")

    users_path = RAW_DIR / "users.csv"
    # orders_path = RAW_DIR / "orders_summary"
    output_orders_path = OUTPUT_DIR / "orders"
    output_path = OUTPUT_DIR / "users_orders_summary"

    users = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(users_path))
    )

    days = sql_func.floor(sql_func.rand() * sql_func.lit(365)).cast("int")

    orders = (
    spark.range(10001, 10301)  # 300 rows
    .withColumn("user_id", (sql_func.floor(sql_func.rand() * 50) + 1).cast("int"))
    .withColumn("amount", (sql_func.rand() * sql_func.lit(300)).cast("decimal(10,2)"))
    .withColumn(
        "created_at",
        sql_func.date_add(
            sql_func.to_date(sql_func.lit("2025-01-01")),
            sql_func.floor(sql_func.rand() * 365).cast("int")
        )
    )
    .select(
        sql_func.col("id").alias("order_id"),
        "user_id",
        "amount",
        "created_at"
    )
    .alias("orders")
)

    # ทำความสะอาด/ปรับชนิดข้อมูลเล็กน้อย (ฝึก cast/parse)
    orders_clean = (
        orders.withColumn("amount", sql_func.col("amount").cast("double"))
        .withColumn("created_at", sql_func.to_timestamp("created_at"))
        .where(sql_func.col("amount").isNotNull())
    )

    (
        orders_clean.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(output_orders_path))
    )

    # join + aggregate
    joined = orders_clean.join(users, on="user_id", how="left")

    summary = (
        joined.groupBy("user_id", "name", "city")
        .agg(
            sql_func.countDistinct("order_id").alias("order_count"),
            sql_func.round(sql_func.sum("amount"), 2).alias("total_amount"),
            sql_func.max("created_at").alias("last_order_at"),
        )
        .orderBy(sql_func.desc("total_amount"), sql_func.desc("order_count"), sql_func.asc("user_id"))
    )

    summary.show(300, truncate=False)

    (
        summary.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(output_path))
    )

    spark.stop()


if __name__ == "__main__":
    main()

