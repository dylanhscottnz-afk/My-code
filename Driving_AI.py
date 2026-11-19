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

epochs = 30
lr = 0.05
Clone_Per_Run = 250

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
    for Num in range(1, 11):
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
    Main_Weights = {'Speed_w1': -0.13386582106702052, 'Speed_w2': 0.0032237751675123633, 'Speed_w3': -0.39218327220052596, 'Speed_w4': 1.052113202822282, 'Speed_w5': 0.03697942853755941, 'Speed_bias': 3.1069132665944372, 'Angle_w1': 0.3196602866284137, 'Angle_w2': -0.041965573602728706, 'Angle_w3': -0.9354779051267024, 'Angle_w4': 0.4327823379042462, 'Angle_w5': 0.9923158982716805, 'Angle_bias': -0.2175053133526179, 1: {'w1': -0.857007964052272, 'w2': 0.9091242120598734, 'w3': 0.27053402929043796, 'w4': 0.7765171824328911, 'w5': -0.2337519611138217, 'bias': 0.5230597821079435}, 2: {'w1': -0.06983795129038403, 'w2': 1.0940602543510807, 'w3': -0.212664492897155, 'w4': -0.039276351989152344, 'w5': -0.23760149888620286, 'bias': -0.9458621988813694}, 3: {'w1': -0.7018760713579054, 'w2': 0.19133286063070395, 'w3': 0.28446936706418163, 'w4': -1.5672337314327431, 'w5': 0.9966003251391867, 'bias': -0.09542015861077975}, 4: {'w1': 1.1548614223679372, 'w2': -0.3173002886111932, 'w3': -1.6238903607990667, 'w4': -1.12024226483802, 'w5': 0.015448515443586719, 'bias': 1.1024143552222256}, 5: {'w1': 0.2291266359858495, 'w2': -1.0032737445310824, 'w3': 0.5866451441008087, 'w4': 0.5733178939936904, 'w5': 0.04441151631708887, 'bias': 0.2147197043568893}, 6: {'w1': -0.20864243511281902, 'w2': -0.09311417027478441, 'w3': -0.44040994550769497, 'w4': -1.154121135597722, 'w5': 0.03258144042881449, 'bias': 0.006766863928689151}, 7: {'w1': -1.2600039072013585, 'w2': -0.8926495853701564, 'w3': -0.01413737231464221, 'w4': -1.1811503431451427, 'w5': -0.6986738020248983, 'bias': -0.7471904219805436}, 8: {'w1': -0.8565361770072576, 'w2': -0.2044603331413685, 'w3': -0.24049560787369448, 'w4': -0.263579364807637, 'w5': 0.6190367632495728, 'bias': 1.1342171593863848}, 9: {'w1': 0.4951207717523948, 'w2': 0.08764120661252806, 'w3': -0.636090741963934, 'w4': -0.5915392364323331, 'w5': 1.439624428509376, 'bias': 1.5803375920527107}, 10: {'w1': 0.32270817771566396, 'w2': -0.6461468906517793, 'w3': 0.6131217285140621, 'w4': -1.2992724406375273, 'w5': 0.3481561763371186, 'bias': -0.04180025537163798}}

    
    
    
    
    
    
    
    
    
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
        Set_Map(5)
        weights = Start_Race(Main_Weights, Clone_Per_Run, 900)
        Main_Weights = weights

        Reset()
    
    Close_GUI()
    print(Main_Weights)

def Test_Model():

    global Main_Weights
    Start_GUI()
    Set_Map(5)
    Start_Race(Main_Weights, 1, 900)
    Close_GUI()

Train(15)