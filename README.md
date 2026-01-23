# pyspark-simple-learning

โปรเจกต์ PySpark แบบ “เล็กและชัด” สำหรับฝึก Spark พื้นฐานบนเครื่อง (local mode) โดยเน้น 3 เรื่อง:

- **อ่านข้อมูล** (text/CSV) → **แปลง/ทำความสะอาด** → **สรุปผล** (group/join/agg)
- **DataFrame API** และ **Spark SQL**
- **เขียนผลลัพธ์** ออกไปเป็นไฟล์เพื่อเปิดดู/ตรวจสอบได้จริง

ในโปรเจกต์นี้มี **data ตัวอย่าง** และ **สคริปต์ตัวอย่าง 3 ตัว** รันได้ทันที:

- `src/jobs/wordcount.py`
- `src/jobs/etl_users_orders.py`
- `src/jobs/sql_demo.py`

---

## สิ่งที่ต้องมี (สำคัญมาก)

### Python

- ใช้ **Python 3.9+** ได้ (เครื่องคุณรันได้ด้วย 3.9.6)
- ถ้าคุณมี 3.10/3.11 ก็ใช้ได้เช่นกัน

> หมายเหตุ: ถ้าเครื่องคุณไม่มีคำสั่ง `python` ให้ใช้ `python3` แทน (macOS พบได้บ่อย)

### Java (จำเป็นสำหรับ Spark)

PySpark ต้องมี Java เพื่อรัน Spark ฝั่ง JVM

- **ถ้าใช้ Java 11** → ควรใช้ **PySpark 3.5.x**
- **ถ้าใช้ Java 17** → ใช้ได้ทั้ง **PySpark 3.5.x** และ **PySpark 4.x**

โปรเจกต์นี้ตั้งใจให้ “รันได้ง่ายบนเครื่องที่มี Java 11” จึง pin ไว้ใน `requirements.txt` เป็น:

- `pyspark>=3.5.0,<4.0`

ตรวจสอบเวอร์ชัน Java:

```bash
java -version
```

ติดตั้ง Java (ตัวอย่าง macOS Homebrew):

```bash
brew install openjdk@11
# หรือ
brew install openjdk@17
```

ตั้ง `JAVA_HOME` (เลือกเวอร์ชันที่คุณติดตั้ง):

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
# หรือ
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

---

## โครงสร้างโฟลเดอร์ (อธิบายละเอียด)

- `src/`
  - `spark_session.py`: ตัวช่วยสร้าง `SparkSession` สำหรับ local
  - `config.py`: path พื้นฐานของโปรเจกต์ (`data/raw`, `data/output`)
  - `jobs/`: สคริปต์เดโมแต่ละงาน (รันด้วย `python -m ...`)
- `data/raw/`
  - `text.txt`: ข้อความสำหรับ wordcount
  - `users.csv`, `orders.csv`: ข้อมูลตัวอย่างสำหรับ ETL/SQL
- `data/output/`
  - โฟลเดอร์ผลลัพธ์ที่ Spark เขียนออกมา
  - มี `README.md` อธิบายไว้

> หมายเหตุ: เวลาสั่ง `df.write.csv("path")` Spark จะสร้าง “โฟลเดอร์” ชื่อ `path/` แล้วมีไฟล์ `part-*.csv` อยู่ข้างใน พร้อมไฟล์ `_SUCCESS` เพื่อบอกว่าเขียนเสร็จสมบูรณ์

---

## (สำหรับคนอยากรู้) โปรเจกต์นี้ถูก “สร้าง” ยังไง

คุณไม่จำเป็นต้องทำเอง แต่ถ้าจะฝึกสร้างใหม่จากศูนย์ แนวคิดคือ:

1) สร้างโฟลเดอร์โปรเจกต์และโครงสร้าง `src/`, `data/raw/`, `data/output/`  
2) ใส่ `requirements.txt` สำหรับ dependency  
3) ใส่สคริปต์ตัวอย่างใน `src/jobs/`  
4) ใส่ data ตัวอย่างลงใน `data/raw/`  
5) เขียน `SparkSession` helper ให้ใช้งานซ้ำได้  

---

## ติดตั้งและเริ่มต้นใช้งาน (แนะนำทำตามทีละบรรทัด)

ไปที่โฟลเดอร์โปรเจกต์:

```bash
cd pyspark-simple-learning
```

สร้าง virtual environment:

```bash
python3 -m venv .venv
```

เปิดใช้งาน venv:

```bash
source .venv/bin/activate
```

อัปเกรด pip และติดตั้ง dependency:

```bash
pip install -U pip
pip install -r requirements.txt
```

---

## “รันทดสอบการติดตั้ง” (Sanity check)

### 1) เช็คว่า Python/Java/พัสดุครบ

```bash
python -V
java -version
python -c "import pyspark; print('pyspark', pyspark.__version__)"
```

สิ่งที่ควรเห็น:

- `java -version` เป็น 11 หรือ 17
- `pyspark` เป็น 3.5.x (เพราะเรา pin `<4.0`)

### 2) เช็คว่า SparkSession สร้างได้ (แบบสั้นที่สุด)

```bash
python -c "from src.spark_session import get_spark; s=get_spark('smoke'); print(s.version); s.stop()"
```

ถ้าตรงนี้ผ่าน แปลว่าสภาพแวดล้อมพร้อมแล้ว

---

## รันเดโมทั้ง 3 ตัว (พร้อมคำอธิบาย + ผลลัพธ์ที่คาดหวัง)

> แนะนำรันจาก root ของโปรเจกต์ (`pyspark-simple-learning/`) และให้เปิด venv แล้ว

### 1) WordCount (DataFrame)

รัน:

```bash
python -m src.jobs.wordcount
```

ทำอะไรบ้าง:

- อ่านไฟล์ `data/raw/text.txt`
- ทำเป็นตัวพิมพ์เล็ก
- split คำด้วย regex `\W+` (ตัดด้วยตัวที่ไม่ใช่ตัวอักษร/ตัวเลข)
- explode เป็น 1 แถวต่อ 1 คำ
- groupBy นับจำนวน
- เขียนผลเป็น CSV ไปที่ `data/output/wordcount/`

ผลลัพธ์ที่คาดหวังบนหน้าจอ (ตัวอย่างจาก data ชุดนี้):

```
+----------+-----+
|word      |count|
+----------+-----+
|is        |4    |
|count     |3    |
|word      |3    |
|for       |2    |
|pyspark   |2    |
... (คำอื่น ๆ) ...
+----------+-----+
```

ไฟล์ผลลัพธ์:

- `data/output/wordcount/part-*.csv`
- `data/output/wordcount/_SUCCESS`

เปิดดูไฟล์ผลลัพธ์แบบง่าย (ตัวอย่างใช้ Python):

```bash
python -c "import glob,pandas as pd; p=glob.glob('data/output/wordcount/part-*.csv')[0]; print(pd.read_csv(p).head(20))"
```

---

### 2) ETL: users + orders (join + aggregate)

รัน:

```bash
python -m src.jobs.etl_users_orders
```

ทำอะไรบ้าง:

- อ่าน `data/raw/users.csv` และ `data/raw/orders.csv` (มี header และใช้ inferSchema)
- ทำความสะอาด `orders`:
  - cast `amount` เป็น double (แถวที่เป็น `N/A` จะกลายเป็น null)
  - parse `created_at` เป็น timestamp
  - กรองแถวที่ `amount` เป็น null ออก
- join กับ `users` ด้วย `user_id` (แบบ `left`)
- groupBy แล้วคำนวณ:
  - `order_count`: จำนวนออเดอร์
  - `total_amount`: ยอดรวม
  - `last_order_at`: เวลาล่าสุด
- เขียนผลเป็น CSV ไปที่ `data/output/users_orders_summary/`

ผลลัพธ์ที่คาดหวังบนหน้าจอ (ตัวอย่างจาก data ชุดนี้):

```
+-------+----+----------+-----------+------------+-------------------+
|user_id|name|city      |order_count|total_amount|last_order_at      |
+-------+----+----------+-----------+------------+-------------------+
|4      |Mai |Phuket    |1          |999.9       |2025-10-05 08:30:00|
|2      |Aom |Chiang Mai|1          |250.0       |2025-12-01 09:00:00|
|1      |Boyd|Bangkok   |2          |159.5       |2025-12-23 18:45:10|
|3      |Ken |Khon Kaen |2          |105.74      |2025-11-12 12:00:00|
|5      |Nok |Bangkok   |1          |60.0        |2025-12-31 23:59:59|
+-------+----+----------+-----------+------------+-------------------+
```

เปิดดูไฟล์ผลลัพธ์:

```bash
python -c "import glob,pandas as pd; p=glob.glob('data/output/users_orders_summary/part-*.csv')[0]; print(pd.read_csv(p))"
```

---

### 3) Spark SQL demo (temp view + SQL query)

รัน:

```bash
python -m src.jobs.sql_demo
```

ทำอะไรบ้าง:

- อ่าน `users.csv` และ `orders.csv`
- สร้าง temp view:
  - `users`
  - `orders`
- ใช้ `spark.sql(...)` เขียน SQL (JOIN + GROUP BY + ORDER BY)

ผลลัพธ์ที่คาดหวังบนหน้าจอ (ตัวอย่าง):

```
+-------+----+----------+-----------+------------+
|user_id|name|city      |order_count|total_amount|
+-------+----+----------+-----------+------------+
|4      |Mai |Phuket    |1          |999.9       |
|2      |Aom |Chiang Mai|2          |250.0       |
|1      |Boyd|Bangkok   |2          |159.5       |
|3      |Ken |Khon Kaen |2          |105.74      |
|5      |Nok |Bangkok   |1          |60.0        |
+-------+----+----------+-----------+------------+
```

> หมายเหตุ: ตัวอย่าง SQL demo จะนับ `order_count` ด้วย `COUNT(DISTINCT o.order_id)` (รวมแถวที่ `amount` เป็น `N/A` ด้วย)  
> ส่วน ETL demo จะ “ลบทิ้ง” แถว `amount` ที่ cast ไม่ได้ก่อน จึงอาจต่างกันได้ในบางเคส (ใน data ชุดนี้ `user_id=2` จะเห็น `order_count` ต่างกัน: SQL = 2, ETL = 1)

---

## การ “รันทดสอบ” แบบตรวจผลลัพธ์จริง (เหมือน checklist)

หลังรันเดโม แนะนำตรวจว่า output ถูกสร้างจริง:

```bash
python -c "import glob; assert glob.glob('data/output/wordcount/part-*.csv'); assert glob.glob('data/output/users_orders_summary/part-*.csv'); print('OK: outputs exist')"
```

ถ้าอยากล้างผลลัพธ์แล้วรันใหม่:

```bash
rm -rf data/output/wordcount data/output/users_orders_summary
```

---

## จุดที่โปรเจกต์นี้ตั้งค่าไว้ให้ “รันง่าย”

ดูที่ `src/spark_session.py`:

- รันแบบ local: `master("local[*]")` (ใช้ทุกคอร์)
- ลดจำนวน shuffle partitions: `spark.sql.shuffle.partitions = 4` (เหมาะกับโปรเจกต์เล็ก)
- ตั้ง timezone เป็น UTC เพื่อให้การแปลงเวลาคงที่
- ที่สำคัญ: บังคับ driver เป็น localhost
  - `spark.driver.bindAddress = 127.0.0.1`
  - `spark.driver.host = 127.0.0.1`

เหตุผลของ localhost config:

- บางเครื่อง (โดยเฉพาะ macOS) อาจเจอ error ตอน Spark สร้าง SparkContext เช่น `UnresolvedAddressException` / ปัญหา hostname/IPv6  
- การบังคับ bind/host เป็น `127.0.0.1` ช่วยให้ Spark เปิดพอร์ต local ได้แน่นอน

---

## Troubleshooting (รวมปัญหาที่เจอบ่อย)

### 1) `ModuleNotFoundError: No module named 'pyspark'`

- ยังไม่ได้ติดตั้ง dependency หรือยังไม่ได้เปิด venv
- แก้โดย:
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`

### 2) `JAVA_GATEWAY_EXITED` / `UnsupportedClassVersionError`

อาการ:

- ถ้าใช้ Spark 4 แต่ Java ต่ำเกินไป จะเจอ `UnsupportedClassVersionError`

แนวทาง:

- ถ้าคุณมี **Java 11** ให้ใช้ **PySpark 3.5.x** (โปรเจกต์นี้ pin ให้แล้ว)
- ถ้าคุณอยากใช้ **PySpark 4.x** ต้องอัปเกรดเป็น **Java 17** และปรับ `requirements.txt` เอา `<4.0` ออก

### 3) `UnresolvedAddressException` ตอนเริ่ม Spark

- มักเกี่ยวกับ hostname/การ bind พอร์ต
- โปรเจกต์นี้แก้ไว้แล้วด้วย `spark.driver.bindAddress/host = 127.0.0.1` ใน `src/spark_session.py`

---

## แนวทางฝึกต่อ (ไอเดียการบ้าน)

ลองแก้/เพิ่มโจทย์ใน `src/jobs/`:

- **เพิ่มคอลัมน์ใหม่** ด้วย `withColumn` (เช่น ทำ bucket ยอดเงิน)
- **filter/where** (เช่น เอาเฉพาะ `city='Bangkok'`)
- **groupBy().agg(...)** เพิ่มค่า `avg(amount)`, `min/max`
- ทดลอง `join` แบบ `inner/left` แล้วเทียบจำนวนแถว
- แยก logic เป็นฟังก์ชันย่อย และเขียน “assert” ตรวจผลลัพธ์ (เช่น row count, ค่า total)
- เปลี่ยน output เป็น **Parquet** แล้วลองอ่านกลับ (`spark.read.parquet`)


