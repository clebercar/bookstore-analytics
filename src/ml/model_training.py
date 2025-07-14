# %%
import pandas as pd
from joblib import dump
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

# %%
df = pd.read_csv("src/ml/books.csv")
df.head()

# %%
features = ["price", "category"]
target = "stars"

X = df[features].copy()
y = df[target].copy()

# %%
category_encoder = LabelEncoder()

X["category"] = category_encoder.fit_transform(X["category"])

# %%
model = tree.DecisionTreeClassifier(max_depth=5)
model.fit(X, y)
# %%
dump(model, "src/ml/model.joblib")
dump(category_encoder, "src/ml/category_encoder.joblib")

print("Model training completed and saved successfully.")
# %%
