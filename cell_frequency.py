# Relative frequency by percentage of each cell type in each sample

import pandas as pd
import sqlite3

conn = sqlite3.connect("cell_count.db")

df = pd.read_sql_query("SELECT * FROM cell_count", conn)

cell_columns = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]

df["total_count"] = df[cell_columns].sum(axis = 1)

cell_frequencies = df.melt(
    id_vars = ["sample", "total_count"],
    value_vars = cell_columns,
    var_name = "population",
    value_name = "count"
)

cell_frequencies["percentage"] = cell_frequencies["count"] / cell_frequencies["total_count"] * 100

cell_frequencies.to_sql("cell_frequencies", conn, if_exists = "replace", index = False)

# CHECK new table added
# tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
# print(tables)

conn.close()
print(cell_frequencies)