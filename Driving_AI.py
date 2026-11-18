import math
import random
import copy
import importlib.util
import sys
from pathlib import Path
import threading
import time

Ai_File = 0

def Locate_Environment():
    filename = "2D_Driving_Environment.py"
    roots = [Path(__file__).resolve().parent, Path.cwd().resolve()]

    for root in roots:
        matches = sorted(root.rglob(filename))
        if matches:
            return matches[0]

    raise FileNotFoundError(f"Cannot find {filename} in the workspace")

def Find_File(Name):
    workspace = Path(".")
    for file in workspace.glob("*.json"):
        if file.Name == "Driving_Ai.json":
            Ai_File = file

    All.Json


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

epochs = 25
lr = 0.1
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

    for i in range(1, 6):
        Weights[f"Speed_w{i}"] += random.uniform(-lr, lr)
        Weights[f"Angle_w{i}"] += random.uniform(-lr, lr)

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
    Main_Weights = {'Speed_w1': -0.1192898731789136, 'Speed_w2': 0.5810281410413594, 'Speed_w3': -0.20929368737171783, 'Speed_w4': 0.04807645345541944, 'Speed_w5': -0.6895417505509078, 'Speed_bias': 1.3698549263231539, 'Angle_w1': -0.3555135156666236, 'Angle_w2': 0.7723312098125882, 'Angle_w3': 0.7193500794131228, 'Angle_w4': -0.7224781693762062, 'Angle_w5': 0.229854808735252, 'Angle_bias': -0.43717619541873437, 1: {'w1': -0.18389839163275293, 'w2': -0.3654319825347921, 'w3': 0.20537327181070975, 'w4': 0.6145639746871395, 'w5': 0.7679300839472517, 'bias': -0.9002965757877445}, 2: {'w1': -0.37921772953499044, 'w2': -0.3519844831466022, 'w3': 0.41466473644748936, 'w4': 0.39880592446404595, 'w5': -0.09156602516545383, 'bias': 0.49829386068519}, 3: {'w1': -0.4369792706654453, 'w2': -0.3018274183128323, 'w3': -0.45107492423294565, 'w4': -0.258624294272222, 'w5': -0.15778046643493077, 'bias': 0.7342505333909078}, 4: {'w1': 0.6536054344616471, 'w2': 0.19240325476621767, 'w3': -0.6055008932420012, 'w4': 0.7501390958950805, 'w5': -0.3947948834031203, 'bias': -0.14196647837054813}, 5: {'w1': -0.47125162906996154, 'w2': 0.719154225214196, 'w3': 0.8034295687646774, 'w4': 0.9453800691075704, 'w5': 0.09065573832572564, 'bias': 1.2073500251650544}, 6: {'w1': 0.09745268813536967, 'w2': 0.9175544848590846, 'w3': 0.6055466470908539, 'w4': -0.3687418422629587, 'w5': 0.07338000553099566, 'bias': 0.18780466544149887}, 7: {'w1': 0.11187313187609926, 'w2': 0.5124948984879623, 'w3': 0.7866607059830937, 'w4': -0.9360514105860065, 'w5': 0.8133602666384643, 'bias': -0.6078110951933509}, 8: {'w1': -0.794915866654059, 'w2': 0.9808998304941103, 'w3': 0.6040380168982229, 'w4': 0.9285700489620612, 'w5': 0.8176529312516523, 'bias': -0.9830663472501047}, 9: {'w1': -0.8403236538688508, 'w2': -0.6386957533869082, 'w3': -0.5123535122405272, 'w4': -0.05199579875330951, 'w5': 0.6047627120354837, 'bias': -0.32696810733062964}, 10: {'w1': -0.08187825189860098, 'w2': 0.47653911543992344, 'w3': -0.30133517688861167, 'w4': 0.9552464993750285, 'w5': -0.8652576616862881, 'bias': 0.19273932061373644}}      
    
    
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

Train(epochs)
