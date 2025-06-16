import pandas as pd

df = pd.read_excel("../data/BaseDefinitivaINDICES-2005-2024.xlsx")
df.to_csv("../data/matriculas.csv")