from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pandas as pd

from app.services.llm_service import generate_explanation

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

    ml_results = train_model(df)

    if "error" not in ml_results:
        explanation = generate_explanation(ml_results)
    else:
        explanation = "ML model could not be generated."

    return {
        "basic_info": basic_info,
        "insights": insights,
        "missing_analysis": missing_info,
        "ml_results": ml_results,
        "llm_explanation": explanation
    }

def train_model(df):
    # Step 1: Select numeric columns only
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:
        return {"error": "Not enough numeric columns for ML"}

    # Step 2: Choose target (last column)
    target_column = numeric_df.columns[-1]

    X = numeric_df.drop(columns=[target_column])
    y = numeric_df[target_column]

    # Step 3: Handle missing values
    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    # Step 4: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Step 5: Train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Step 6: Predictions
    y_pred = model.predict(X_test)

    # Step 7: Evaluate
    score = r2_score(y_test, y_pred)

    # Step 8: Feature importance
    importance = dict(zip(X.columns, model.feature_importances_))

    return {
        "target_column": target_column,
        "model_score": round(score, 3),
        "feature_importance": importance
    }