import pandas as pd
import matplotlib.pyplot as plt

# Load your file + sheet
df = pd.read_excel("Comp370_Data.xlsx", sheet_name="Final Annotations for tf-idf wi")

# Count topics
topic_counts = df['annotation'].value_counts()

# Colors — one unique color per slice
colors = plt.cm.Set3(range(len(topic_counts)))

plt.figure(figsize=(10, 10))

# Create pie chart
plt.pie(
    topic_counts.values,           # sizes
    labels=topic_counts.index,     # topic names
    autopct='%1.1f%%',             # show % values
    startangle=140,                # rotate for better layout
    colors=colors
)

# Title
plt.title("Topic Breakdown of Articles in the Trump News Dataset", fontsize=20)

plt.tight_layout()
plt.savefig("topic_distribution_pie.png", dpi=200)
plt.show()
