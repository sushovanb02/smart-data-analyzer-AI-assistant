import pandas as pd

def analyze_data(file_path):
    df = pd.read_csv(file_path)

    basic_info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
    }

    # Select only numeric columns
    numeric_df = df.select_dtypes(include=['number'])

    insights = {}

    if not numeric_df.empty:
        # Correlation matrix
        corr_matrix = numeric_df.corr()

        # Flatten correlations and sort
        corr_pairs = (
            corr_matrix.unstack()
            .reset_index()
        )
        corr_pairs.columns = ["feature_1", "feature_2", "correlation"]

        # Remove self-correlation
        corr_pairs = corr_pairs[corr_pairs["feature_1"] != corr_pairs["feature_2"]]

        # Sort by absolute correlation
        corr_pairs["abs_corr"] = corr_pairs["correlation"].abs()
        top_corr = corr_pairs.sort_values(by="abs_corr", ascending=False).head(5)

        insights["top_correlations"] = top_corr[
            ["feature_1", "feature_2", "correlation"]
        ].to_dict(orient="records")

    missing_percentage = (df.isnull().sum() / len(df)) * 100

    missing_info = {}

    for col, pct in missing_percentage.items():
        if pct == 0:
            status = "clean"
        elif pct < 20:
            status = "moderate"
        else:
            status = "high_missing"

    missing_info[col] = {
        "missing_percent": round(pct, 2),
        "status": status
    }

    return {
        "basic_info": basic_info,
        "insights": insights,
        "missing_analysis": missing_info
    }