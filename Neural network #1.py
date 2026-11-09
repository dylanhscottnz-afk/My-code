import math
import random



data = [
    {"Value1": 0, "Value2": 0, "Output": 0},
    {"Value1": 0, "Value2": 1, "Output": 1},
    {"Value1": 8, "Value2": 3, "Output": 11},
    {"Value1": 0, "Value2": 0, "Output": 0},
    {"Value1": 0, "Value2": 1, "Output": 1},
    {"Value1": 8, "Value2": 3, "Output": 11},
]


random.seed(49)
w_1 = random.uniform(-1, 1)
w_2 = random.uniform(-1, 1)
bias = random.uniform(-1, 1)

learning_rate = 0.01
epochs = 1000


for epoch in range(epochs):
    for d in data:
        x1 = d["Value1"]
        x2 = d["Value2"]
        target = d["Output"]

        Ans = (w_1 * x1) + (w_2 * x2) + bias

        error = Ans - target

        # Update weights and bias
        w_1 -= learning_rate * error * x1
        w_2 -= learning_rate * error * x2
        bias -= learning_rate * error
        



Num1 = 12
Num2 = 3

print(round((w_1 * Num1) + (w_2 * Num2) + bias, 3))