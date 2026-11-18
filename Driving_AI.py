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

def Set_Map(Map_Number):
    return Env.Set_Map(Map_Number)

epochs = 10
lr = 0.05
Clone_Per_Run = 100

Raycast1 = 2
Raycast2 = 3
Raycast3 = 0
Speed = 0.5
Angle = 0

N = {}
Answers = {}
Answers2 = {}
Training_Clones = {}
Car_Info = {}

def Edit_Weights(Weights):
    Weights = copy.deepcopy(Weights)
    for Num in range(1, 6):
        for W in range(1, 6):
            Weights[Num][f"w{W}"] += random.uniform(-lr, lr)
        Weights[Num]["bias"] += random.uniform(-lr, lr)

    for i in range(5):
        Weights[f"Speed_w{i+1}"] += random.uniform(-lr, lr)
        Weights[f"Angle_w{i+1}"] += random.uniform(-lr, lr)

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

if False:
    Main_Weights = {
        "Speed_w1": random.uniform(-1, 1),
        "Speed_w2": random.uniform(-1, 1),
        "Speed_w3": random.uniform(-1, 1),
        "Speed_w4": random.uniform(-1, 1),
        "Speed_w5": random.uniform(-1, 1),
        "Speed_bias": random.uniform(-1, 1),
        "Angle_w1": random.uniform(-1, 1),
        "Angle_w2": random.uniform(-1, 1),
        "Angle_w3": random.uniform(-1, 1),
        "Angle_w4": random.uniform(-1, 1),
        "Angle_w5": random.uniform(-1, 1),
        "Angle_bias": random.uniform(-1, 1),
        1: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        2: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        3: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        4: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        5: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        6: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        7: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        8: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        9: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
        10: {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        },
    }


else:
    Main_Weights = {'w1': -0.05287417027328234, 'w2': 0.679829865697915, 'w3': 0.24079001791963012, 'w4': -0.5808080310372988, 'w5': 0.6547910459982553, 'bias': 0.34601015606162805}, 2: {'w1': 0.1969061029360939, 'w2': -0.8812088646249268, 'w3': -0.6504614101925505, 'w4': -0.6482808803065185, 'w5': 0.6058115274192573, 'bias': -0.13565384745230102}, 3: {'w1': -0.9685646727020242, 'w2': 1.608885842386388, 'w3': -0.26874025123011464, 'w4': -0.36406593743652654, 'w5': 0.43307298347351925, 'bias': 0.721086427026127}, 4: {'w1': -0.6577030735399346, 'w2': 0.4663754495170027, 'w3': 1.5121521216612999, 'w4': -0.49223346135308255, 'w5': 0.3953107317864818, 'bias': 0.4170412421469216}, 5: {'w1': 0.14975012314808536, 'w2': 0.8810887052197827, 'w3': -1.2062320872072503, 'w4': -0.4438185129876775, 'w5': -0.5807738840226464, 'bias': 1.2500524693238155}, 6: {'w1': 0.949640164899068, 'w2': -0.16733024598572643, 'w3': 0.05454803784990836, 'w4': -0.29431654375657956, 'w5': 0.059381671828249605, 'bias': 0.10046119147694443}, 7: {'w1': 0.6397298048544262, 'w2': 0.8444580508599953, 'w3': -0.6307415153557108, 'w4': 0.24058101521329123, 'w5': -0.7248793952022885, 'bias': -0.16817149201004922}, 8: {'w1': -0.4427119803324586, 'w2': -0.7950045565709956, 'w3': 0.5410408439154641, 'w4': -0.28714726963367143, 'w5': -0.8797122307805365, 'bias': 0.0910674176473738}, 9: {'w1': 0.17225084310540084, 'w2': -0.30444913335008983, 'w3': 0.40587157711538535, 'w4': 0.49847991371931655, 'w5': 0.8242997970498029, 'bias': -0.7221138698666629}, 10: {'w1': 0.1416140133713657, 'w2': -0.8444177190275686, 'w3': -0.8161445001095344, 'w4': 0.7549478991069491, 'w5': -0.33410090252284963, 'bias': 0.6670339272096519}}     
    
    
def Get_Outputs(Weights, Raycast1, Raycast2, Raycast3, Speed, Angle):
    Raycast1 = min(Raycast1 / 400, 1)
    Raycast2 = min(Raycast2 / 400, 1)
    Raycast3 = min(Raycast3 / 400, 1)
    Normalied_Angle = (Angle / 180) - 1
    Answers = {}
    for Neuron in range(1, 6):
        
        Ans = math.tanh((Raycast1 * Weights[Neuron]["w1"]) + (Raycast2 * Weights[Neuron]["w2"]) + (Raycast3 * Weights[Neuron]["w3"]) + (Speed * Weights[Neuron]["w4"]) + (Normalied_Angle * Weights[Neuron]["w5"]) + Weights[Neuron]["bias"])
        Answers[f"Ans{Neuron}"] = Ans

    for Neuron in range(6, 11):
        Ans = math.tanh((Answers["Ans1"] * Weights[Neuron]["w1"]) + (Answers["Ans2"] * Weights[Neuron]["w2"]) + (Answers["Ans3"] * Weights[Neuron]["w3"]) + (Answers["Ans4"] * Weights[Neuron]["w4"]) + (Answers["Ans5"] * Weights[Neuron]["w5"]) + Weights[Neuron]["bias"])
        Answers2[f"Ans{Neuron-5}"] = Ans
    
    Speed_Ans = (
        (math.tanh(
        (Answers2["Ans1"] * Weights["Speed_w1"]) + (Answers2["Ans2"] * Weights["Speed_w2"]) + (Answers2["Ans3"] * Weights["Speed_w3"]) + (Answers2["Ans4"] * Weights["Speed_w4"]) + (Answers2["Ans5"] * Weights["Speed_w5"]) + Weights["Speed_bias"])
        +1)
        / 2
    )
    Angle_Ans = (
        Angle + math.tanh(
            (Answers2["Ans1"] * Weights["Angle_w1"]) +
            (Answers2["Ans2"] * Weights["Angle_w2"]) +
            (Answers2["Ans3"] * Weights["Angle_w3"]) +
            (Answers2["Ans4"] * Weights["Angle_w4"]) +
            (Answers2["Ans5"] * Weights["Angle_w5"]) +
            Weights["Angle_bias"]
        ) * 45
    ) % 360
    
    return Speed_Ans, Angle_Ans

def Create_Clones(Starting_Weights, Num_Clones):
    global Training_Clones
    for i in range(Num_Clones-1):
        Training_Clones[f"Clone{i+1}"] = Edit_Weights(Starting_Weights)
    Training_Clones[f"Clone{Num_Clones}"] = Starting_Weights
    

def Drive(Weights, num):
    CarID = num

    while Car_Info[num]["Alive"] and not Check_Progress(CarID)["crashed"]:
        Info = Get_Info(CarID)
        Progress = Check_Progress(CarID)

        Speed, Angle = Get_Outputs(
            Weights,
            Info["raycast1"],
            Info["raycast2"],
            Info["raycast3"],
            Info["speed"],
            Info["angle"]
        )

        Change_Value(CarID, Speed, Angle)
        Car_Info[num]["Score"] = Progress["reward"]

        time.sleep(1 / 30)

    Car_Info[num]["Alive"] = False




def Start_Race(Weight, Amount, RaceTime):
    global Training_Clones, Car_Info

    Training_Clones = {}
    Car_Info = {}
    Create_Clones(Weight, Amount)
    Threads = []

    for Car in Training_Clones:
        Spawn_Car(Car)
        Car_Info[Car] = {"Alive": True, "Score": 0}


    for Car in Training_Clones:
        Thread = threading.Thread(
            target=Drive,
            args=(Training_Clones[Car], Car),
            daemon=True
        )
        Thread.start()
        Threads.append(Thread)

    Alive = len(Training_Clones)
    Runs = 0

    while Alive != 0 and Runs < RaceTime:
        Update()
        Render()
        Runs += 1

        Alive = 0
        for Car in Training_Clones:
            if not Check_Progress(Car)["crashed"]:
                Alive += 1

    for Car in Training_Clones:
        Car_Info[Car]["Alive"] = False

    for Thread in Threads:
        Thread.join()

    for Car in Training_Clones:
        Car_Info[Car]["Score"] = Check_Progress(Car)["reward"]

    CarNum = max(Car_Info, key=lambda Car: Car_Info[Car]["Score"])
    print("Winner:", CarNum, "Score:", Car_Info[CarNum]["Score"])

    return Training_Clones[CarNum]


def Train(Repeats):
    global Main_Weights
    global Training_Clones
    global Car_Info
    Start_GUI()
    weights = Main_Weights
    Map = 0
    for i in range(Repeats):
        Map += 1
        if Map > 5:
            Map -= 5
        Set_Map(Map)
        weights = Start_Race(Main_Weights, Clone_Per_Run, 900)
        Main_Weights = weights

        Reset()
    
    Close_GUI()
    print(Main_Weights)

def Test_Model():

    global Main_Weights
    Start_GUI()
    Set_Map(1)
    Start_Race(Main_Weights, 1, 900)
    Close_GUI()

Train(30)