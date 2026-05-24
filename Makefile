setup:
	pip install -r requirements.txt

pipeline:
	python3 load_data.py
	python3 cell_frequency.py
	python3 response_comparison.py
	python3 subset_analysis.py

dashboard:
	streamlit run dashboard.py