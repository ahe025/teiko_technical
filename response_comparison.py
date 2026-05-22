# Compare differences in cell population relative frequencies of melanoma patients 
# receiving miraclib who respond (responders) versus those who do not (non-responders),
# only including PBMC samples.

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

conn = sqlite3.connect("cell_count.db")

query = "WHERE condition == 'melanoma'" \
        "AND treatment == 'miraclib'" \
        "AND sample_type == 'PBMC'"
query_yes = query + "AND response == 'yes'"
query_no = query + "AND response == 'no'"

fig, axes = plt.subplots(2, 3, figsize = (12, 8))
axes = axes.flatten()

populations = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
mwu_results = []

for i, cell in enumerate(populations):
    response_yes = pd.read_sql_query("SELECT percentage FROM cell_frequencies " \
                                     "WHERE population == '" + cell + "'" \
                                     "AND sample IN (SELECT sample FROM cell_count " \
                                     + query_yes + ")", conn)
    response_no = pd.read_sql_query("SELECT percentage FROM cell_frequencies " \
                                    "WHERE population == '" + cell + "'" \
                                    "AND sample IN (SELECT sample FROM cell_count " \
                                    + query_no + ")", conn)
    axes[i].boxplot([response_yes["percentage"].tolist(), response_no["percentage"].tolist()], labels = ['Responders', 'Non-responders'])
    axes[i].set_title(cell + ' Relative frequencies (%)')

    # Mann-Whitney U test
    u_statistic, p_value = mannwhitneyu(response_yes["percentage"], response_no["percentage"], alternative = "two-sided")
    mwu_results.append({
        "population": cell,
        "responders_mean": response_yes["percentage"].mean(),
        "nonresponders_mean": response_no["percentage"].mean(),
        "p_value": p_value,
        "significant": p_value < 0.05
    })

axes[5].set_visible(False)
fig.suptitle("Cell population relative frequencies in responders vs. non-responders (Melanoma patients receiving miraclib, PBMC samples only)")
plt.tight_layout()
plt.show()

mwu_results_df = pd.DataFrame(mwu_results)
print(mwu_results_df)

mwu_results_df.to_sql("mwu_results", conn, if_exists = "replace", index = False)

conn.close()