import pandas as pd

df = pd.read_csv("savings.csv", encoding="utf-8", sep="\t")


month = df.Month.tolist()
expenses = df.Expenses.tolist()
savings = df.Savings.tolist()
budget = df.Budget.tolist()

# print(month)
