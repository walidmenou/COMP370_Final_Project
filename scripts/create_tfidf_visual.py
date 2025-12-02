import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

INPUT_CSV = "data/tf_idf_top_words.csv"
OUT_DIR = "visuals"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_CSV)

def safe_name(s):
    name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in s)
    name = name.strip().replace(" ", "_")
    while "__" in name:
        name = name.replace("__", "_")
    return name.strip("_")

for _, row in df.iterrows():
    topic = row["topic"]
    words = []
    scores = []
    for i in range(1, 11):
        w_col = f"word_{i}"
        s_col = f"score_{i}"
        if pd.notna(row.get(w_col)):
            words.append(row[w_col])
            scores.append(float(row.get(s_col, 0.0)))

    if not words:
        continue

    pairs = sorted(zip(words, scores), key=lambda ws: ws[1], reverse=True)
    words_sorted, scores_sorted = zip(*pairs)

    plt.figure(figsize=(8, max(3, len(words_sorted) * 0.4)))
    sns.barplot(x=list(scores_sorted), y=list(words_sorted), palette="viridis")
    plt.xlabel("TF-IDF score")
    plt.title(f"Top words — {topic}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f"{safe_name(topic)}_bar.png"))
    plt.close()