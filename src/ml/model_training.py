# %%
# %%
import os

import pandas as pd
from joblib import dump
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "books.csv"))
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
dump(model, os.path.join(script_dir, "model.joblib"))
dump(category_encoder, os.path.join(script_dir, "category_encoder.joblib"))

print("Model training completed and saved successfully.")
# %%
