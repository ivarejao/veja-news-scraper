import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

names = ["agenda_verde", "cultura", "mundo", "saude"]

files = {"Setor":[], "Quantidade":[]}

for n in names:
    print(n)
    with open("../data/{}/links.txt".format(n), "r") as f:
        lines = f.read()
        files["Quantidade"].append(len(lines))
        files["Setor"].append(n)

df = pd.DataFrame(files, columns=["Setor", "Quantidade"])
print(df)
sns.set_theme()
sns.barplot(data=df, x="Setor", y="Quantidade")
plt.savefig("../dist_sector.png")
