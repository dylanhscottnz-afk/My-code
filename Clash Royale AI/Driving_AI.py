import math
import random

epochs = 1000
lr = 0.01

Raycast1 = 2
Raycast2 = 3
Raycast3 = 0
Speed = 0.5
Angle = 0

N = {}
Answers = {}
Main_Weights = {}


def Edit_Weights(Weights):
    for Num in range(5):
        for W in range(5):
            N[Num][W] += random.uniform(-0.2, 0.2)

for Run in range(5):
    Neuron = Run + 1
    
    N[Neuron] = {}

    N[Neuron]["w1"] = random.uniform(-1, 1)
    N[Neuron]["w2"] = random.uniform(-1, 1)
    N[Neuron]["w3"] = random.uniform(-1, 1)
    N[Neuron]["w4"] = random.uniform(-1, 1)
    N[Neuron]["w5"] = random.uniform(-1, 1)
    N[Neuron]["bias"] = random.uniform(-1, 1)

    Ans = (Raycast1 * N[Neuron]["w1"]) + (Raycast2 * N[Neuron]["w2"]) + (Raycast3 * N[Neuron]["w3"]) + (Speed * N[Neuron]["w4"]) + (Angle * N[Neuron]["w5"]) + N[Neuron]["bias"]
    Answers[f"Ans{Neuron}"] = Ans

    
Speed_w1 = random.uniform(-1, 1)
Speed_w2 = random.uniform(-1, 1)
Speed_w3 = random.uniform(-1, 1)
Speed_w4 = random.uniform(-1, 1)
Speed_w5 = random.uniform(-1, 1)
Speed_bias = random.uniform(-1, 1)

Speed = (
    (Answers["Ans1"] * Speed_w1) +
    (Answers["Ans2"] * Speed_w2) +
    (Answers["Ans3"] * Speed_w3) +
    (Answers["Ans4"] * Speed_w4) +
    (Answers["Ans5"] * Speed_w5) +
    Speed_bias
)