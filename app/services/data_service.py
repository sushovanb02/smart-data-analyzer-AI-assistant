import pandas as pd

def analyze_data(file_path):
    df = pd.read_csv(file_path)

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "summary": df.describe().to_dict()
    }