# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

with open("spo.jl") as f:
    tuples = [eval(line.strip()) for line in f.readlines()]


# %%
relation = dict()
for spo in tuples:
    pred = spo["pred"]
    if pred in relation.keys():
        relation[pred] += 1
    else:
        relation[pred] = 1

# 按value排序一遍
relation = {
    k: v for k, v in sorted(relation.items(), key=lambda item: item[1], reverse=True)
}


# %%
print(f"共有{len(relation)}种关系\n次数最多的前20种关系如下：")
for key in list(relation)[:20]:
    print(f"{key}: {relation[key]}")


# %%
plt.figure(figsize=(10, 18))
x = list(relation)[:5] + ["其他"]
y = list(relation.values())[:5] + [sum(list(relation.values())[5:])]
# 画柱状图
plt.subplot(211)
plt.bar(range(len(y)), y, width=0.3)
plt.xticks(range(len(x)), x, fontsize="small", rotation=30)
for i, j in enumerate(y):
    plt.text(i, j + 30, j, horizontalalignment="center", fontsize="small")
plt.title("次数最多的前5种关系之柱状分析图")
# 画饼图
plt.subplot(212)
y = list(relation.values())[:20] + [sum(list(relation.values())[20:])]
labels = list(relation)[:20] + ["其他"]
colors = cm.nipy_spectral_r([1.0 * i / len(y) for i in range(len(y))])
plt.pie(
    y, labels=labels, autopct="%.1f%%", textprops={"fontsize": "small"}, colors=colors
)
plt.axis("equal")
plt.title("次数最多的前20种关系之饼状分析图")
plt.savefig("figure.png")
plt.show()


# %%

