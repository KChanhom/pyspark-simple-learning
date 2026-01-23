from __future__ import annotations

from pyspark.sql import SparkSession


def get_spark(app_name: str) -> SparkSession:
    """
    สร้าง SparkSession สำหรับรันบนเครื่อง (local mode)

    ปรับ config ให้เหมาะกับโปรเจกต์เล็ก ๆ:
    - ลด shuffle partitions เพื่อให้เร็วขึ้นบนเครื่อง
    """
    spark = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        # บังคับให้ driver bind/advertise เป็น localhost เพื่อเลี่ยงปัญหา
        # hostname/IPv6 บางเครื่องที่ resolve/bind ไม่ได้ (เจอได้บ่อยบน macOS)
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    # ลด log noise เวลาฝึก
    spark.sparkContext.setLogLevel("WARN")
    return spark

