import pandas as pd
import sqlite3

df = pd.read_csv("cell-count.csv")

conn = sqlite3.connect("cell_count.db")

df.to_sql("cell_count", conn, if_exists = "replace", index = False)

# CHECKS
# df_check = pd.read_sql_query("SELECT * FROM cell_count", conn)
# print(df_check.head())

# schema_info = pd.read_sql_query("PRAGMA table_info(cell_count)", conn)
# print(schema_info)

# print(df.shape)
# print(df_check.shape)

conn.close()
print("Database created successfully.")