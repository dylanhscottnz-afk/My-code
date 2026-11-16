import math
import random
import copy
import importlib.util
import sys
from pathlib import Path
import threading
import time

def Locate_Environment():
    filename = "2D_Driving_Environment.py"
    roots = [Path(__file__).resolve().parent, Path.cwd().resolve()]

    for root in roots:
        matches = sorted(root.rglob(filename))
        if matches:
            return matches[0]

    raise FileNotFoundError(f"Cannot find {filename} in the workspace")

def Load_Environment():
    path = Locate_Environment()
    spec = importlib.util.spec_from_file_location("DrivingEnvironment", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

Env = Load_Environment()

def Spawn_Car(Name=None):
    # Returns the new car's ID (name or number)
    return Env.Spawn_Car(Name)

def Get_Info(CarID):
    # Returns a dictionary with raycast1, raycast2, raycast3, speed, angle, crashed, lap, elapsed, progress and best_lap_time
    return Env.Get_Info(CarID)

def Change_Value(CarID, Speed, Angle):
    # Sets target speed (0-1) and angle (0-360); returns nothing
    return Env.Change_Value(CarID, Speed, Angle)

def Check_Progress(CarID):
    # Returns crashed, distance, forward_progress, fastest_lap_time, laps, elapsed and reward
    return Env.Check_Progress(CarID)

def Get_Rewards(CarID):
    # Returns a dictionary containing the car's reward values
    return Env.Get_Rewards(CarID)

def Update():
    # Advances all cars by one frame; returns nothing
    return Env.Update()

def Reset():
    # Removes all cars and resets the race; returns nothing
    return Env.Reset()

def Start_GUI():
    # Opens the 2D driving window; returns nothing
    return Env.Start_GUI()

def Render():
    # Updates the driving window; returns nothing
    return Env.Render()

def Close_GUI():
    # Closes the driving window; returns nothing
    return Env.Close_GUI()
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
Training_Clones = {}
Car_Info = {}

def Edit_Weights(Weights):
    Weights = copy.deepcopy(Weights)
    for Num in range(1, 6):
        for W in range(1, 6):
            Weights[Num][f"w{W}"] += random.uniform(-0.2, 0.2)
        Weights[Num]["bias"] += random.uniform(-0.2, 0.2)

    for i in range(5):
        Weights[f"Speed_w{i+1}"] += random.uniform(-0.2, 0.2)
        Weights[f"Angle_w{i+1}"] += random.uniform(-0.2, 0.2)

    Weights["Speed_bias"] += random.uniform(-0.2, 0.2)
    Weights["Angle_bias"] += random.uniform(-0.2, 0.2)
    return Weights

for Neuron in range(1, 6):
    N[Neuron] = {}

    N[Neuron]["w1"] = random.uniform(-1, 1)
    N[Neuron]["w2"] = random.uniform(-1, 1)
    N[Neuron]["w3"] = random.uniform(-1, 1)
    N[Neuron]["w4"] = random.uniform(-1, 1)
    N[Neuron]["w5"] = random.uniform(-1, 1)
    N[Neuron]["bias"] = random.uniform(-1, 1)

    Ans = (Raycast1 * N[Neuron]["w1"]) + (Raycast2 * N[Neuron]["w2"]) + (Raycast3 * N[Neuron]["w3"]) + (Speed * N[Neuron]["w4"]) + (Angle * N[Neuron]["w5"]) + N[Neuron]["bias"]

Speed_w1 = random.uniform(-1, 1)
Speed_w2 = random.uniform(-1, 1)
Speed_w3 = random.uniform(-1, 1)
Speed_w4 = random.uniform(-1, 1)
Speed_w5 = random.uniform(-1, 1)
Speed_bias = random.uniform(-1, 1)

Angle_w1 = random.uniform(-1, 1)
Angle_w2 = random.uniform(-1, 1)
Angle_w3 = random.uniform(-1, 1)
Angle_w4 = random.uniform(-1, 1)
Angle_w5 = random.uniform(-1, 1)
Angle_bias = random.uniform(-1, 1)



Main_weights = {
    "Speed_w1": Speed_w1,
    "Speed_w2": Speed_w2,
    "Speed_w3": Speed_w3,
    "Speed_w4": Speed_w4,
    "Speed_w5": Speed_w5,
    "Speed_bias": Speed_bias,
    "Angle_w1": Angle_w1,
    "Angle_w2": Angle_w2,
    "Angle_w3": Angle_w3,
    "Angle_w4": Angle_w4,
    "Angle_w5": Angle_w5,
    "Angle_bias": Angle_bias,
    1: {
        "w1": N[1]["w1"],
        "w2": N[1]["w2"],
        "w3": N[1]["w3"],
        "w4": N[1]["w4"],
        "w5": N[1]["w5"],
        "bias": N[1]["bias"]
    },
    2: {
        "w1": N[2]["w1"],
        "w2": N[2]["w2"],
        "w3": N[2]["w3"],
        "w4": N[2]["w4"],
        "w5": N[2]["w5"],
        "bias": N[2]["bias"]
    },
    3: {
        "w1": N[3]["w1"],
        "w2": N[3]["w2"],
        "w3": N[3]["w3"],
        "w4": N[3]["w4"],
        "w5": N[3]["w5"],
        "bias": N[3]["bias"]
    },
    4: {
        "w1": N[4]["w1"],
        "w2": N[4]["w2"],
        "w3": N[4]["w3"],
        "w4": N[4]["w4"],
        "w5": N[4]["w5"],
        "bias": N[4]["bias"]
    },
    5: {
        "w1": N[5]["w1"],
        "w2": N[5]["w2"],
        "w3": N[5]["w3"],
        "w4": N[5]["w4"],
        "w5": N[5]["w5"],
        "bias": N[5]["bias"]
    }
}

def Get_Outputs(Weights, Raycast1, Raycast2, Raycast3, Speed, Angle):
    Answers = {}
    for Neuron in range(1, 6):
        
        Ans  = math.tanh((Raycast1 * Weights[Neuron]["w1"]) + (Raycast2 * Weights[Neuron]["w2"]) + (Raycast3 * Weights[Neuron]["w3"]) + (Speed * Weights[Neuron]["w4"]) + (Angle * Weights[Neuron]["w5"]) + Weights[Neuron]["bias"])
        Answers[f"Ans{Neuron}"] = Ans
    
    Speed_Ans = (
        (math.tanh(
        (Answers["Ans1"] * Weights["Speed_w1"]) + (Answers["Ans2"] * Weights["Speed_w2"]) + (Answers["Ans3"] * Weights["Speed_w3"]) + (Answers["Ans4"] * Weights["Speed_w4"]) + (Answers["Ans5"] * Weights["Speed_w5"]) + Weights["Speed_bias"])
        +1)
        /2
    )
    Angle_Ans = (
        (math.tanh(
        (Answers["Ans1"] * Weights["Angle_w1"]) + (Answers["Ans2"] * Weights["Angle_w2"]) + (Answers["Ans3"] * Weights["Angle_w3"]) + (Answers["Ans4"] * Weights["Angle_w4"]) + (Answers["Ans5"] * Weights["Angle_w5"]) + Weights["Angle_bias"])
        +1)
        *180
    )
    
    return Speed_Ans, Angle_Ans

def Create_Clones(Starting_Weights, Num_Clones):
    for i in range(Num_Clones):
        Training_Clones[f"Clone{i+1}"] = Edit_Weights(Starting_Weights)
    

def Drive(Weights, num):
    CarID = Spawn_Car(f"{num}")
    Progress = Check_Progress(CarID)

    while Progress["crashed"] != True:
        Info = Get_Info(CarID)
        Progress = Check_Progress(CarID)
        raycast1 = Info["raycast1"]
        raycast2 = Info["raycast2"]
        raycast3 = Info["raycast3"]
        speed = Info["speed"]
        angle = Info["angle"]
        Speed, Angle = Get_Outputs(Weights, raycast1, raycast2, raycast3, speed, angle)
        Change_Value(CarID, Speed, Angle)
        Car_Info[num] = {
            "Alive": not Progress["crashed"],
        }
        time.sleep(1/30)
    Progress = Check_Progress(CarID)
    Score = 
    

def Start_Race(Weight, Amount):
    Create_Clones(Weight, Amount)
    Start_GUI()



    for i in Training_Clones:
        threading.Thread(
            target=Drive,
            args=(Training_Clones[i], i),
            daemon=True
        ).start()

    Alive = len(Training_Clones)
    time.sleep(0.4)
    while Alive != 0:
        Update()
        Render()

        Alive = 0

        for Car in Training_Clones:
            Progress = Check_Progress(Car)

            if not Progress["crashed"]:
                Alive += 1

        time.sleep(1 / 30)

    Close_GUI()


def Train():
    Start_Race(Main_Weights, 20)
    



Start_Race()