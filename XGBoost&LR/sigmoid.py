'''
@Time    : 2020/5/6 21:14
@Author  : sh_lord
@FileName: sigmoid.py

'''
import math
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

X = list(range(-10, 10))
Y = list(map(sigmoid, X))

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111)

ax.spines["top"].set_color("none")
ax.spines["right"].set_color("none")

ax.yaxis.set_ticks_position("left")
# y轴位于0处
ax.spines["left"].set_position(("data", 0))
ax.xaxis.set_ticks_position("bottom")
# x轴位于0.5处， x,y 交叉于（0,0.5）
ax.spines["bottom"].set_position(("data", 0.5))

ax.plot(X, Y)
plt.show()