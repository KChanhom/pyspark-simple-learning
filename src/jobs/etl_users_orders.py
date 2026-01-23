from __future__ import annotations

from pyspark.sql import functions as F

from src.config import OUTPUT_DIR, RAW_DIR
from src.spark_session import get_spark


def main() -> None:
    spark = get_spark("etl_users_orders")

    users_path = RAW_DIR / "users.csv"
    orders_path = RAW_DIR / "orders.csv"
    output_path = OUTPUT_DIR / "users_orders_summary"

    users = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(users_path))
    )

    orders = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(orders_path))
    )

    # ทำความสะอาด/ปรับชนิดข้อมูลเล็กน้อย (ฝึก cast/parse)
    orders_clean = (
        orders.withColumn("amount", F.col("amount").cast("double"))
        .withColumn("created_at", F.to_timestamp("created_at"))
        .where(F.col("amount").isNotNull())
    )

    # join + aggregate
    joined = orders_clean.join(users, on="user_id", how="left")

    summary = (
        joined.groupBy("user_id", "name", "city")
        .agg(
            F.countDistinct("order_id").alias("order_count"),
            F.round(F.sum("amount"), 2).alias("total_amount"),
            F.max("created_at").alias("last_order_at"),
        )
        .orderBy(F.desc("total_amount"), F.desc("order_count"), F.asc("user_id"))
    )

    summary.show(50, truncate=False)

    (
        summary.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(output_path))
    )

    spark.stop()


if __name__ == "__main__":
    main()

