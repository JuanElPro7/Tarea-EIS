import pandas as pd

df = pd.read_excel("../data/OfertaPregrado2025.xlsx")
df.to_csv("../data/ofertasPregrado2025.csv")