import psycopg2
from faker import Faker

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

# Create the table
cur.execute("""
    CREATE TABLE example_table (
        id SERIAL PRIMARY KEY,
        large_column TEXT
    )
""")

# Generate large data
fake = Faker()
data_size = 1 * 1024 * 1024 * 1024  # 2 GB in bytes
chunk_size = 1000  # Adjust as per your system resources

while data_size > 0:
    chunk_data = [(fake.text(),) for _ in range(min(chunk_size, data_size))]
    cur.executemany("INSERT INTO example_table (large_column) VALUES (%s)", chunk_data)
    conn.commit()
    data_size -= chunk_size

# Close the cursor and connection
cur.close()
conn.close()
