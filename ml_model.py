# ml_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from typing import List

class LabelSuggestionModel:
    def __init__(self, csv_path="label_pairs.csv"):
        self.csv_path = csv_path
        self.load()

    def load(self):
        self.data = pd.read_csv(self.csv_path)

        # 🛡️ Remove duplicate headers if accidentally appended
        self.data = self.data[self.data["parent"] != "parent"]

        # 🔠 Normalize all labels to lowercase
        self.data["parent"] = self.data["parent"].str.lower()

        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.data["parent"])
        self.y = self.data["child"]
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.model.fit(self.X, self.y)

    def suggest(self, parent_label: str, k: int = 3) -> List[str]:
        x = self.vectorizer.transform([parent_label.lower()])
        preds = self.model.kneighbors(x, n_neighbors=k, return_distance=False)
        suggestions = [self.y.iloc[i] for i in preds[0]]
        print(f"[ML DEBUG] Suggestions for '{parent_label}': {suggestions}")
        return suggestions

# global model instance
ml_suggester = LabelSuggestionModel()

