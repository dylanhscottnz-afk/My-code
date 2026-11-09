import math
import random



data = [
    {"Value1": 0, "Value2": 0, "Output": 0},
    {"Value1": 0, "Value2": 1, "Output": 1},
    {"Value1": 8, "Value2": 3, "Output": 11},
    {"Value1": 12, "Value2": 3, "Output": 15},
    {"Value1": 2, "Value2": 5, "Output": 7},
    {"Value1": 7, "Value2": 9, "Output": 16},
    {"Value1": 4, "Value2": 6, "Output": 10},
    {"Value1": 15, "Value2": 8, "Output": 23},
    {"Value1": 20, "Value2": 10, "Output": 30},
    {"Value1": 13, "Value2": 17, "Output": 30},
    {"Value1": 25, "Value2": 35, "Output": 60},
    {"Value1": 40, "Value2": 12, "Output": 52},
    {"Value1": 19, "Value2": 21, "Output": 40},
    {"Value1": 33, "Value2": 44, "Output": 77},
    {"Value1": 50, "Value2": 50, "Output": 100},
    {"Value1": 61, "Value2": 29, "Output": 90},
    {"Value1": 75, "Value2": 15, "Output": 90},
    {"Value1": 88, "Value2": 12, "Output": 100},
    {"Value1": 99, "Value2": 1, "Output": 100},
    {"Value1": 45, "Value2": 67, "Output": 112},
    {"Value1": 100, "Value2": 200, "Output": 300},
    {"Value1": 125, "Value2": 75, "Output": 200},
    {"Value1": 150, "Value2": 350, "Output": 500},
    {"Value1": 234, "Value2": 123, "Output": 357},
    {"Value1": 500, "Value2": 250, "Output": 750},
    {"Value1": 678, "Value2": 321, "Output": 999},
    {"Value1": 999, "Value2": 1, "Output": 1000},
    {"Value1": 456, "Value2": 789, "Output": 1245},
    {"Value1": 800, "Value2": 120, "Output": 920},
    {"Value1": 375, "Value2": 625, "Output": 1000},
    {"Value1": 1000, "Value2": 2000, "Output": 3000},
    {"Value1": 1234, "Value2": 5678, "Output": 6912},
    {"Value1": 2500, "Value2": 7500, "Output": 10000},
    {"Value1": 4321, "Value2": 1234, "Output": 5555},
    {"Value1": 9999, "Value2": 1, "Output": 10000},
    {"Value1": 3456, "Value2": 6544, "Output": 10000},
    {"Value1": 5000, "Value2": 3000, "Output": 8000},
    {"Value1": 7890, "Value2": 1110, "Output": 9000},
    {"Value1": 6000, "Value2": 4000, "Output": 10000},
    {"Value1": 8765, "Value2": 4321, "Output": 13086},
    {"Value1": 10000, "Value2": 20000, "Output": 30000},
    {"Value1": 12345, "Value2": 54321, "Output": 66666},
    {"Value1": 25000, "Value2": 75000, "Output": 100000},
    {"Value1": 45678, "Value2": 12345, "Output": 58023},
    {"Value1": 99999, "Value2": 1, "Output": 100000},
    {"Value1": 50000, "Value2": 25000, "Output": 75000},
    {"Value1": 87654, "Value2": 12346, "Output": 100000},
    {"Value1": 34567, "Value2": 76543, "Output": 111110},
    {"Value1": 80000, "Value2": 15000, "Output": 95000},
    {"Value1": 65432, "Value2": 34568, "Output": 100000},
    {"Value1": 100000, "Value2": 200000, "Output": 300000},
    {"Value1": 123456, "Value2": 654321, "Output": 777777},
    {"Value1": 500000, "Value2": 250000, "Output": 750000},
    {"Value1": 999999, "Value2": 1, "Output": 1000000},
    {"Value1": 345678, "Value2": 123456, "Output": 469134},
    {"Value1": 750000, "Value2": 125000, "Output": 875000},
    {"Value1": 888888, "Value2": 111111, "Output": 999999},
    {"Value1": 456789, "Value2": 987654, "Output": 1444443},
    {"Value1": 600000, "Value2": 400000, "Output": 1000000},
    {"Value1": 234567, "Value2": 765433, "Output": 1000000},
    {"Value1": 1000000, "Value2": 2000000, "Output": 3000000},
    {"Value1": 1234567, "Value2": 7654321, "Output": 8888888},
    {"Value1": 5000000, "Value2": 2500000, "Output": 7500000},
    {"Value1": 9999999, "Value2": 1, "Output": 10000000},
    {"Value1": 3456789, "Value2": 1234567, "Output": 4691356},
    {"Value1": 8000000, "Value2": 1500000, "Output": 9500000},
    {"Value1": 6543210, "Value2": 3456790, "Output": 10000000},
    {"Value1": 7777777, "Value2": 2222222, "Output": 9999999},
    {"Value1": 4567890, "Value2": 9876543, "Output": 14444433},
    {"Value1": 6000000, "Value2": 4000000, "Output": 10000000},
    {"Value1": 0, "Value2": 999, "Output": 999},
    {"Value1": 500, "Value2": 0, "Output": 500},
    {"Value1": 1, "Value2": 100000, "Output": 100001},
    {"Value1": 999999, "Value2": 0, "Output": 999999},
    {"Value1": 42, "Value2": 10000, "Output": 10042},
    {"Value1": 7, "Value2": 500000, "Output": 500007},
    {"Value1": 123, "Value2": 99999, "Output": 100122},
    {"Value1": 8888, "Value2": 2, "Output": 8890},
    {"Value1": 1000000, "Value2": 5, "Output": 1000005},
    {"Value1": 25, "Value2": 750000, "Output": 750025},
    {"Value1": -5, "Value2": 10, "Output": 5},
    {"Value1": -20, "Value2": 7, "Output": -13},
    {"Value1": 50, "Value2": -30, "Output": 20},
    {"Value1": -100, "Value2": -200, "Output": -300},
    {"Value1": -999, "Value2": 1000, "Output": 1},
    {"Value1": 500, "Value2": -750, "Output": -250},
    {"Value1": -1234, "Value2": 5678, "Output": 4444},
    {"Value1": 10000, "Value2": -5000, "Output": 5000},
    {"Value1": -25000, "Value2": 75000, "Output": 50000},
    {"Value1": -999999, "Value2": 999999, "Output": 0},
    {"Value1": 3, "Value2": 9997, "Output": 10000},
    {"Value1": 17, "Value2": 83, "Output": 100},
    {"Value1": 111, "Value2": 222, "Output": 333},
    {"Value1": 12345, "Value2": 67890, "Output": 80235},
    {"Value1": 98765, "Value2": 43210, "Output": 141975},
    {"Value1": 123456, "Value2": 789012, "Output": 912468},
    {"Value1": 3456789, "Value2": 6543211, "Output": 10000000},
    {"Value1": 9876543, "Value2": 1234567, "Output": 11111110},
    {"Value1": 12345678, "Value2": 87654322, "Output": 100000000},
    {"Value1": 50000000, "Value2": 50000000, "Output": 100000000},
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

print((w_1 * Num1) + (w_2 * Num2) + bias)