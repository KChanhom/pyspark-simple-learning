from __future__ import annotations

from src.config import OUTPUT_DIR, RAW_DIR
from src.spark_session import get_spark
from pyspark.sql import functions as sql_func


def main() -> None:
    spark = get_spark("sql_demo")
    output_path = OUTPUT_DIR / "orders_summary"

    users = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(RAW_DIR / "users.csv"))
    )
 
    orders = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(OUTPUT_DIR / "orders/part-*.csv"))
    )

    users.createOrReplaceTempView("users")
    orders.createOrReplaceTempView("orders")

    result = spark.sql(
        """
        SELECT
          u.user_id,
          u.name,
          u.city,
          COUNT(DISTINCT o.order_id) AS order_count,
          ROUND(SUM(CAST(o.amount AS DOUBLE)), 2) AS total_amount
        FROM users u
        LEFT JOIN orders o
          ON u.user_id = o.user_id
        GROUP BY u.user_id, u.name, u.city
        ORDER BY total_amount DESC, order_count DESC, u.user_id ASC
        """
    )

    result.show(50, truncate=False)

    (
        result.coalesce(1)
        .write.mode("overwrite")
        .option("header", True)
        .csv(str(output_path))
    )

    spark.stop()


if __name__ == "__main__":
    main()

