import pandas as pd
import sqlite3
import streamlit as st

with sqlite3.connect("cell_count.db") as conn:

    st.title("Data Analysis Dashboard: Immune Cell Populations")

    # Part 1
    cell_count = pd.read_sql_query("SELECT * FROM cell_count", conn)
    with st.expander("See original cell-count.csv (raw data)"):
        st.subheader("Cell Count")
        st.text("Relational database from original cell-count.csv")
        st.dataframe(cell_count)

    # Part 2
    cell_frequencies = pd.read_sql_query("SELECT * FROM cell_frequencies", conn)
    st.header("Cell Frequency")
    st.text("Relative frequency (by percentage) of each cell type in each sample")
    st.dataframe(cell_frequencies)

    # Part 3
    st.header("Statistical Analysis")
    st.subheader("Boxplot")
    st.text("Compares differences in cell population relative frequencies of melanoma patients " \
            "receiving miraclib who respond (responders) versus those who do not (non-responders), only including PBMC samples.")
    st.image("boxplots.png")

    mwu_results = pd.read_sql_query("SELECT * FROM mwu_results", conn)
    st.subheader("Mann-Whitney U Test")
    st.text("Reports which cell populations have a significant difference in relative frequencies between " \
            "responders and non-responders.")
    st.dataframe(mwu_results)
    st.caption("0 = False (Not significant); 1 = True (Significant)")

    # Part 4
    st.header("Data Subset Analysis")
    baseline_data = pd.read_sql_query("SELECT * FROM baseline_data", conn)
    project_count = pd.read_sql_query("SELECT * FROM project_count", conn)
    response_count = pd.read_sql_query("SELECT * FROM response_count", conn)
    sex_count = pd.read_sql_query("SELECT * FROM sex_count", conn)

    st.subheader("Baseline set: All melanoma PBMC samples at baseline (time = 0) from patients treated with miraclib")
    st.dataframe(baseline_data)

    st.subheader("Project count: Number of samples from each project among Baseline set")
    st.dataframe(project_count)

    st.subheader("Number of subjects who were responders/non-responders among Baseline set")
    st.dataframe(response_count)

    st.subheader("Number of subjects who were males/females among Baseline set")
    st.dataframe(sex_count)