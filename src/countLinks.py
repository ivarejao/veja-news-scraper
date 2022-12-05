# Code made in Pycharm by Igor Varejao

years = list(range(2008, 2015))

sum = 0
for y in years:
    with open(f"../data/links-{y}.txt", "r") as r:
        sum += len(r.readlines())

print(sum)


if __name__ == "__main__":
    pass
