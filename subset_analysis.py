# Identify subsets of melanoma PBMC samples from patients treated with miraclib
# at time_from_treatment_start = 0.

import pandas as pd
import sqlite3

conn = sqlite3.connect("cell_count.db")

# Baseline set: All melanoma PBMC samples at baseline from patients treated with miraclib
query = "WHERE condition == 'melanoma'" \
        "AND treatment == 'miraclib'" \
        "AND sample_type == 'PBMC'" \
        "AND time_from_treatment_start == 0"
baseline_df = pd.read_sql_query("SELECT * FROM cell_count " + query, conn)
print(baseline_df)
baseline_df.to_sql("baseline_data", conn, if_exists = "replace", index = False)

# Out of baseline set:
# Number of samples from each project
project_count = baseline_df["project"].value_counts().reset_index()
project_count.columns = ["project", "sample_count"]
print(project_count)

# Number of subjects who were responders/non-responders
response_count = baseline_df.groupby("response")["subject"].nunique().reset_index()
response_count.columns = ["response", "subject_count"]
print(response_count)

# Number of subjects who were males/females
sex_count = baseline_df.groupby("sex")["subject"].nunique().reset_index()
sex_count.columns = ["sex", "subject_count"]
print(sex_count)

project_count.to_sql("project_count", conn, if_exists = "replace", index = False)
response_count.to_sql("response_count", conn, if_exists = "replace", index = False)
sex_count.to_sql("sex_count", conn, if_exists = "replace", index = False)

conn.close()