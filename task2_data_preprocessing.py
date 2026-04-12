import json
import pandas as pd

filename = r"C:\ProgFiles\IIT-PATNA\Trendpulse-SanjayKumarDupati\data/hacker_news_stories_20260412_230659.json"
with open(filename, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df)

print("Duplicate entries: ", df.duplicated().sum())