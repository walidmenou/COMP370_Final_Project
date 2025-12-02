import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Load your dataframe
df = pd.read_excel("Comp370_Data.xlsx", sheet_name="Final Annotations for tf-idf wi")


# Create Topic × Sentiment summary table
pivot = pd.crosstab(df['annotation'], df['Sentiments'])

# Ensure consistent order of sentiment columns
pivot = pivot[['Positive', 'Neutral', 'Negative']]  # reorder if needed

# Setup positions
topics = pivot.index
sentiments = pivot.columns

x = np.arange(len(topics))     # x locations for topics
width = 0.25                   # width of each bar

plt.figure(figsize=(14, 7))

# Assign colors for each sentiment
colors = ["#5f986d", "#2C6295", '#c44e52']  # green, blue, red

# Create one bar series for each sentiment
for i, sentiment in enumerate(sentiments):
    plt.bar(x + i*width, pivot[sentiment], 
            width=width, 
            label=sentiment,
            color=colors[i])

# Formatting
plt.title("Sentiment Distribution Across Topics", fontsize=16)
plt.xlabel("Topics", fontsize=14)
plt.ylabel("Number of Articles", fontsize=14)
plt.xticks(x + width, topics, rotation=45, ha='right')

plt.legend(title="Sentiment", fontsize=12)
plt.tight_layout()

plt.show()
