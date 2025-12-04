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

topics_data = []
global_max = 0.0
for _, row in df.iterrows():
    topic = row["topic"]
    words = []
    scores = []
    for i in range(1, 11):
        w_col = f"word_{i}"
        s_col = f"score_{i}"
        if pd.notna(row.get(w_col)):
            words.append(str(row[w_col]))
            scores.append(float(row.get(s_col, 0.0)))

    if not words:
        continue

    pairs = sorted(zip(words, scores), key=lambda ws: ws[1], reverse=True)
    words_sorted, scores_sorted = zip(*pairs)

    topics_data.append((topic, list(words_sorted), list(scores_sorted)))
    if max(scores_sorted) > global_max:
        global_max = max(scores_sorted)

sns.set_style("whitegrid")
for topic, words, scores in topics_data:
    plt.figure(figsize=(8, max(3, len(words) * 0.4)))
    sns.barplot(x=list(scores), y=list(words), palette="viridis")
    plt.xlabel("TF-IDF score")
    plt.title(f"Top words — {topic}")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, f"{safe_name(topic)}_bar.png"))
    plt.close()

if topics_data:
    n = len(topics_data)
    fig, axes = plt.subplots(nrows=n, ncols=1, figsize=(12, 2.5 * n), constrained_layout=True)
    if n == 1:
        axes = [axes]

    for ax, (topic, words, scores) in zip(axes, topics_data):
        x = range(len(words))
        ax.bar(x, scores, color="C0")
        ax.set_xticks(x)
        ax.set_xticklabels(words, rotation=45, ha="right")
        ax.set_ylim(0, global_max * 1.05 if global_max > 0 else None)
        ax.set_title(topic, loc="center", fontsize=10)
        ax.set_ylabel("TF-IDF")

    fig.suptitle("TF-IDF Scores for Each Category", fontsize=14, y=1.02)
    out_path = os.path.join(OUT_DIR, "all_topics_bars.png")
    fig.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close(fig)