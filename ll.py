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

# Create the table with 30 columns
create_table_query = """
    CREATE TABLE example_table (
        id SERIAL PRIMARY KEY,
        """ + ", ".join([f"column_{i} TEXT" for i in range(1, 31)]) + """
    )
"""
cur.execute(create_table_query)

# Generate large data
fake = Faker()
data_size = 30000  # Number of rows to insert
chunk_size = 1000   # Adjust as per your system resources

while data_size > 0:
    chunk_data = [(fake.text(),) * 30 for _ in range(min(chunk_size, data_size))]
    cur.executemany("INSERT INTO example_table (column_1, column_2, column_3, column_4, column_5, \
                     column_6, column_7, column_8, column_9, column_10, \
                     column_11, column_12, column_13, column_14, column_15, \
                     column_16, column_17, column_18, column_19, column_20, \
                     column_21, column_22, column_23, column_24, column_25, \
                     column_26, column_27, column_28, column_29, column_30) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", chunk_data)
    data_size -= chunk_size

# Create indexes on all columns
for i in range(1, 31):
    cur.execute(f"CREATE INDEX idx_column_{i} ON example_table (column_{i})")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
