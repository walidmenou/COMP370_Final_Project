import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_CSV = "data/article_annotation_data.csv"
OUTPUT_CSV = "data/tf_idf_top_words.csv"
TOP_N_WORDS = 10

def main():
    df = pd.read_csv(INPUT_CSV)

    required_cols = {"title", "description", "annotation"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    
    # df[column_name].astype(str) would be nan if empty
    df["description"] = df["description"].fillna("")
    df["title"] = df["title"].fillna("")

    df["text"] = df["title"].astype(str) + " " + df["description"].astype(str)

    df = df.dropna(subset=["annotation"])

    grouped = df.groupby("annotation")["text"].apply(lambda rows: " ".join(rows))

    annotation_topics = grouped.index.tolist()
    articles_by_topic = grouped.values.tolist()

    # compute TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english", # remove common English words
        max_df=0.90, # ignore words that appear in more than 90% of articles (e.g. the)
        min_df=2 # requires words to appear in at least 2 articles
    )
    
    tf_idf_matrix = vectorizer.fit_transform(articles_by_topic) # one row per topic and one column per word
    feature_names = vectorizer.get_feature_names_out()

    results = []

    for index, topic in enumerate(annotation_topics):
        row = tf_idf_matrix.getrow(index).toarray().flatten()
        top_indices = row.argsort()[::-1][:TOP_N_WORDS]

        # creates tuple list of (word, tf-idf score)
        word_list = [(feature_names[i], float(row[i])) for i in top_indices]

        results.append({
            "topic": topic,
            "top_words": word_list
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()
