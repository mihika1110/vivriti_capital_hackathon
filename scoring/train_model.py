import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

data={
    "ebitda_margin": [0.05, 0.12, 0.2, 0.08, 0.15, 0.03],
    "gst_mismatch": [20, 5, 0, 18, 3, 30],
    "bank_mismatch": [1, 0, 0, 1, 0, 1],
    "litigation": [1, 0, 0, 1, 0, 1],
    "capacity_util": [40, 75, 85, 45, 80, 30],
    "default": [1, 0, 0, 1, 0, 1]
}

df=pd.DataFrame(data)

X=df.drop("default", axis=1)
y=df["default"]

model=LogisticRegression(
    solver="liblinear",
    max_iter=1000
)

model.fit(X, y)

joblib.dump(model, "scoring/credit_model.pkl")

print("✅ Credit model trained and saved successfully")