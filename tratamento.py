# %%
import pandas as pd

df = pd.read_csv("Java_zmap.csv")

print(df.head())

# %%

df = pd.read_json("Java_results.json", lines=True)

df.head()


# %%
df.drop(columns=["favicon","pluginCount","ping", "players", "modInfo", "software", "timestamp", "serverType", "tags", "motd_normalized"], inplace = True)
df.columns

# %%
df.to_csv("dados.csv", index=False)
# %%
