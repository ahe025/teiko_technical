# Compare differences in cell population relative frequencies of melanoma patients 
# receiving miraclib who respond (responders) versus those who do not (non-responders),
# only including PBMC samples.

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("cell_count.db")

query = "WHERE condition == 'melanoma'" \
        "AND treatment == 'miraclib'" \
        "AND sample_type == 'PBMC'"
query_yes = query + "AND response == 'yes'"
query_no = query + "AND response == 'no'"

fig, axes = plt.subplots(2, 3, figsize = (12, 8))
axes = axes.flatten()

populations = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
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

axes[5].set_visible(False)
fig.suptitle("Cell population relative frequencies in responders vs. non-responders (Melanoma patients receiving miraclib, PBMC samples only)")
plt.tight_layout()
plt.show()