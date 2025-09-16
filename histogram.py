import matplotlib.pyplot as plt
import pandas as pd
import json

# Load raw JSON
with open("evaluation.json") as f:
    raw = json.load(f)

# Flatten nested list of lists into a single list of dicts
flat_data = []
for group in raw:
    if isinstance(group, list):
        flat_data.extend(group)
    elif isinstance(group, dict):
        flat_data.append(group)

# Convert to DataFrame
df = pd.DataFrame(flat_data)
df_clean = df[["Criteria.name", "Criteria.score", "Criteria.explanation"]].dropna()


# Convert DataFrame to list of dictionaries
#data_to_write = df_clean.to_dict(orient="records")

#with open("histogram_data.txt", "w") as file:
#    json.dump(data_to_write, file, indent=2)  # indent=2 for pretty formatting

# Normalize Criteria.name: strip spaces, lowercase
df_clean["Criteria.name"] = df_clean["Criteria.name"].str.strip().str.lower()

# Group by Criteria.name
grouped = df_clean.groupby("Criteria.name")["Criteria.score"].apply(list)

fig, axes = plt.subplots(1, len(grouped), figsize=(12, 4), sharey=True)

if len(grouped) == 1:
    axes = [axes]

for ax, (criteria, scores) in zip(axes, grouped.items()):
    ax.hist(scores, bins=range(1, 12), edgecolor="black", align="left")
    ax.set_title(criteria, fontsize=14)
    ax.set_xlabel("score", fontsize=14)
    ax.set_ylabel("frequency", fontsize=14)
    ax.set_xticks(range(1, 11))
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)  # horizontal lines

plt.suptitle("Histograms of Criteria Scores", fontsize=14)
plt.tight_layout()
plt.show()