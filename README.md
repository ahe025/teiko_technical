# Teiko Technical
Data analysis of cell count information for various immune cell populations of patient samples.

## Instructions
Run the Python programs in the following order:
1. Data Management: [load_data.py](https://github.com/ahe025/teiko_technical/blob/main/load_data.py)
2. Initial Analysis - Data Overview: [cell_frequency.py](https://github.com/ahe025/teiko_technical/blob/main/cell_frequency.py)
3. Statistical Analysis: [response_comparison.py](https://github.com/ahe025/teiko_technical/blob/main/response_comparison.py)
4. Data Subset Analysis: [subset_analysis.py](https://github.com/ahe025/teiko_technical/blob/main/subset_analysis.py)

## Explanation of schema used for relational database
* This relational database uses an SQLite table (`cell_count` in [cell_count.db](https://github.com/ahe025/teiko_technical/blob/main/cell_count.db)) in which each row represents one sample, and columns store associated metadata (project, subject, condition, treatment, response, demographics, and sample type) with immune cell counts. This schema is simple and efficient for analysis, filtering, and aggregation using SQL/pandas.
* For larger-scale datasets with hundreds of projects and thousands of samples, the schema could be normalized into related tables such as `projects`, `subjects`, `samples`, and `cell_counts`, linked through primary and foreign keys. This design would improve query performance and support more advanced analytics such as longitudinal analysis, multi-treatment comparisons, and integration of additional cell populations or assay types.

## Code structure overview and design explanation

### Initial Analysis - Data Overview: [cell_frequency.py](https://github.com/ahe025/teiko_technical/blob/main/cell_frequency.py)
* In `cell_count`, the total count of all cell populations is first calculated and added as the column `total_count`.
* The `cell_count` DataFrame is then melted so that each sample holds five rows for each of the five cell populations. Now, the relative frequencies of each population are calculated as a percentage, and this data is stored in `cell_frequencies`.
* The `cell_frequencies` table is saved as an SQLite Database to [cell_count.db](https://github.com/ahe025/teiko_technical/blob/main/cell_count.db).

### Statistical Analysis: [response_comparison.py](https://github.com/ahe025/teiko_technical/blob/main/response_comparison.py)
* `query` stores a string specifying the desired query of melanoma PBMC samples from patients treated with miraclib. `query_yes` and `query_no` add specifications for responders and non-responders, respectively.
* To create one plot for each cell population, a for loop iterates over each cell population. `response_yes` and `response_no` use `query_yes` and `query_no` (resp.) to aggregate data over the desired responder and non-reponder groups. The distribution of cell population percentages for responders and non-responders are plotted as a box plot.
* All five box plots are displayed in one figure for easy side-by-side viewing and comparisons. This figure is saved.
* The Mann-Whitney U test is used for statistical analysis to determine which cell populations have a significant difference in relative frequencies between responders and non-responders. MWU is favored as it is non-parametric, robust (outliers do not heavily skew the mean), and is a common choice in immune cell data analysis.
* The MWU test results, `mwu_results`, are saved as an SQLite Database to [cell_count.db](https://github.com/ahe025/teiko_technical/blob/main/cell_count.db).

### Data Subset Analysis: [subset_analysis.py](https://github.com/ahe025/teiko_technical/blob/main/subset_analysis.py)
* `query` stores a string specifying the desired query of all melanoma PBMC samples at baseline (time = 0) from patients treated with miraclib. `baseline_df` stores this specified set using `query`, and this set saved as an SQLite Database, `baseline_data`, to [cell_count.db](https://github.com/ahe025/teiko_technical/blob/main/cell_count.db).
* To count the number of samples from each project, pandas `value_counts()` is used on the `project` column of `baseline_df`.
* To count the number of subjects who were responders/non-responders and males/females, pandas `groupby()` is first used on the `response` or `sex` categories, then the `subject` column is selected, and `nunique()` is called. Since we are counting subjects instead of samples, this method does not assume that the number of subjects equals the number of samples (although it is true in this case).
* The counts `project_count`, `response_count`, and `sex_count` are saved as SQLite Databases to [cell_count.db](https://github.com/ahe025/teiko_technical/blob/main/cell_count.db).

## Dashboard link
[link here](google.com)