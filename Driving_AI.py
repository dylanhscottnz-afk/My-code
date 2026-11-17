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
Clone_Per_Run = 500

Raycast1 = 2
Raycast2 = 3
Raycast3 = 0
Speed = 0.5
Angle = 0

N = {}
Answers = {}
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
    Main_Weights = { "Speed_w1": Speed_w1, "Speed_w2": Speed_w2, "Speed_w3": Speed_w3, "Speed_w4": Speed_w4, "Speed_w5": Speed_w5, "Speed_bias": Speed_bias, "Angle_w1": Angle_w1, "Angle_w2": Angle_w2, "Angle_w3": Angle_w3, "Angle_w4": Angle_w4, "Angle_w5": Angle_w5, "Angle_bias": Angle_bias, 1: { "w1": N[1]["w1"], "w2": N[1]["w2"], "w3": N[1]["w3"], "w4": N[1]["w4"], "w5": N[1]["w5"], "bias": N[1]["bias"] }, 2: { "w1": N[2]["w1"], "w2": N[2]["w2"], "w3": N[2]["w3"], "w4": N[2]["w4"], "w5": N[2]["w5"], "bias": N[2]["bias"] }, 3: { "w1": N[3]["w1"], "w2": N[3]["w2"], "w3": N[3]["w3"], "w4": N[3]["w4"], "w5": N[3]["w5"], "bias": N[3]["bias"] }, 4: { "w1": N[4]["w1"], "w2": N[4]["w2"], "w3": N[4]["w3"], "w4": N[4]["w4"], "w5": N[4]["w5"], "bias": N[4]["bias"] }, 5: { "w1": N[5]["w1"], "w2": N[5]["w2"], "w3": N[5]["w3"], "w4": N[5]["w4"], "w5": N[5]["w5"], "bias": N[5]["bias"] } }
else:
    Main_Weights = {'Speed_w1': 0.796536583653853, 'Speed_w2': 0.22615713243379773, 'Speed_w3': 0.6234122280654826, 'Speed_w4': -0.22027721437330866, 'Speed_w5': 1.1171746893322971, 'Speed_bias': 2.8491066604611426, 'Angle_w1': -1.4052456338507735, 'Angle_w2': -0.6092271772395608, 'Angle_w3': -0.015173348009286637, 'Angle_w4': 1.0075086063206022, 'Angle_w5': 0.2208286313060719, 'Angle_bias': 0.0987057232102348, 1: {'w1': 1.000842043625676, 'w2': 0.582826061697384, 'w3': -0.5833310580093811, 'w4': 0.050948446656464655, 'w5': -0.026264591539791278, 'bias': 0.21599184349964232}, 2: {'w1': 0.867116584683447, 'w2': -0.9749268110291949, 'w3': -1.0348875197037881, 'w4': 0.22875168949004737, 'w5': 0.04421531923359412, 'bias': 0.38974419823987433}, 3: {'w1': 0.637435372053074, 'w2': -0.4422311633295174, 'w3': 0.3267903072213215, 'w4': 0.051388833276485066, 'w5': -0.7757039038778688, 'bias': 0.5897607512085983}, 4: {'w1': -0.4349923258507262, 'w2': -0.5120769217019586, 'w3': 1.182911084162373, 'w4': -0.06968980269483682, 'w5': -0.14791871773068382, 'bias': 0.7415699998756828}, 5: {'w1': 0.5930985208936138, 'w2': 0.6612152217012288, 'w3': 0.10502706605683068, 'w4': 0.2524824054104977, 'w5': 0.038891781664160005, 'bias': 0.6712380634236212}}
    
    
def Get_Outputs(Weights, Raycast1, Raycast2, Raycast3, Speed, Angle):
    Raycast1 = min(Raycast1 / 400, 1)
    Raycast2 = min(Raycast2 / 400, 1)
    Raycast3 = min(Raycast3 / 400, 1)
    Normalied_Angle = (Angle / 180) - 1
    Answers = {}
    for Neuron in range(1, 6):
        
        Ans  = math.tanh((Raycast1 * Weights[Neuron]["w1"]) + (Raycast2 * Weights[Neuron]["w2"]) + (Raycast3 * Weights[Neuron]["w3"]) + (Speed * Weights[Neuron]["w4"]) + (Normalied_Angle * Weights[Neuron]["w5"]) + Weights[Neuron]["bias"])
        Answers[f"Ans{Neuron}"] = Ans
    
    Speed_Ans = (
        (math.tanh(
        (Answers["Ans1"] * Weights["Speed_w1"]) + (Answers["Ans2"] * Weights["Speed_w2"]) + (Answers["Ans3"] * Weights["Speed_w3"]) + (Answers["Ans4"] * Weights["Speed_w4"]) + (Answers["Ans5"] * Weights["Speed_w5"]) + Weights["Speed_bias"])
        +1)
        / 2
    )
    Angle_Ans = (
        Angle + math.tanh(
            (Answers["Ans1"] * Weights["Angle_w1"]) +
            (Answers["Ans2"] * Weights["Angle_w2"]) +
            (Answers["Ans3"] * Weights["Angle_w3"]) +
            (Answers["Ans4"] * Weights["Angle_w4"]) +
            (Answers["Ans5"] * Weights["Angle_w5"]) +
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
        weights = Start_Race(Main_Weights, Clone_Per_Run, 600)
        Main_Weights = weights

        Reset()
    
    Close_GUI()
    print(Main_Weights)

def Test_Model():
    Start_GUI()
    Set_Map(5)
    Start_Race(Main_Weights, 1, 1500)
    Close_GUI()

Test_Model()