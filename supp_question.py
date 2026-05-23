# Considering Melanoma males, what is the average number of B cells for responders at time=0? 

import pandas as pd
import sqlite3

conn = sqlite3.connect("cell_count.db")

df = pd.read_sql_query("SELECT b_cell FROM cell_count " \
                       "WHERE sex == 'M'" \
                       "AND condition == 'melanoma'" \
                       "AND response == 'yes'" \
                       "AND time_from_treatment_start == 0", conn)

print(df.mean()) # 10206.150515

conn.close()