from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

from app.services.llm_service import generate_explanation
from app.services.llm_client import get_llm

def analyze_data(file_path):
    df = pd.read_csv(file_path)

    basic_info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
    }

    numeric_df = df.select_dtypes(include=['number'])

    insights = {}

    if not numeric_df.empty:
        corr_matrix = numeric_df.corr()

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
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:
        return {"error": "Not enough numeric columns for ML"}

    target_column = numeric_df.columns[-1]

    X = numeric_df.drop(columns=[target_column])
    y = numeric_df[target_column]

    X = X.fillna(X.mean())
    y = y.fillna(y.mean())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    score = r2_score(y_test, y_pred)

    importance = dict(zip(X.columns, model.feature_importances_))

    return {
        "target_column": target_column,
        "model_score": round(score, 3),
        "feature_importance": importance
    }

def ask_question(file_path, question):
    df = pd.read_csv(file_path)

    sample_data = df.head(5).to_string()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a highly skilled data analyst.

            Your job:
            - Understand datasets
            - Answer user questions accurately
            - Perform reasoning when needed

            Rules:
            - Be precise
            - Use the dataset context
            - If unsure, say you are unsure
            """
        ),
        (
            "human",
            """
            Dataset sample:
            {data}

            Question:
            {question}
            """
        )
    ])

    llm = llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
        "data": sample_data,
        "question": question
    })

    return response.content