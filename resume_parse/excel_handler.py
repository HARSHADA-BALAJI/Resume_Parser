import pandas as pd
import os

EXCEL_FILE = "resume_job_matches.xlsx"

def append_to_excel(data: dict):
    # data keys: 'Resume', 'Score', 'Explanation'
    df_new = pd.DataFrame([data])
    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_excel(EXCEL_FILE, index=False)

