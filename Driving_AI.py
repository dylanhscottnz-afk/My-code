import copy
import importlib.util
import json
import math
from pathlib import Path
import random
import sys


def Locate_Environment():
    filename = "2D_Driving_Environment.py"
    roots = [Path(__file__).resolve().parent, Path.cwd().resolve()]
    for root in roots:
        matches = sorted(root.rglob(filename))
        if matches:
            return matches[0]
    raise FileNotFoundError(f"Cannot find {filename} in the workspace")


def Find_File():
    workspace = Path(".")
    AllJsonfiles = list(workspace.rglob("*.json"))
    for file in AllJsonfiles:
        if file.name == "Driving_AI.json":
            return file
    return Path("Driving_AI.json")


def Get_File_Contents(file_path):
    if file_path is None or not file_path.exists():
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return {int(k) if k.isdigit() else k: v for k, v in data.items()}


def Write_File_Contents(file_path, info):
    if file_path is None:
        print("Cannot save: no file path provided.")
        return
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4)


def Load_Environment():
    path = Locate_Environment()
    spec = importlib.util.spec_from_file_location("DrivingEnvironment", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


Env = Load_Environment()


def Spawn_Car(Name=None):
    return Env.Spawn_Car(Name)


def Get_Info(CarID):
    return Env.Get_Info(CarID)


def Change_Value(CarID, Speed, Angle):
    return Env.Change_Value(CarID, Speed, Angle)


def Check_Progress(CarID):
    return Env.Check_Progress(CarID)


def Get_Rewards(CarID):
    return Env.Get_Rewards(CarID)


def Update():
    return Env.Update()


def Reset():
    return Env.Reset()


def Start_GUI():
    return Env.Start_GUI()


def Render():
    return Env.Render()


def Close_GUI():
    return Env.Close_GUI()


def Set_Map(Map_Number):
    return Env.Set_Map(Map_Number)


epochs = 25
lr = 0.1
Clone_Per_Run = 100
TRAIN = True
TrainWithPreData = False

Training_Clones = {}
Car_Info = {}


def Create_Random_Weights():
    weights = {
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
    }
    for n in range(1, 11):
        weights[n] = {
            "w1": random.uniform(-1, 1),
            "w2": random.uniform(-1, 1),
            "w3": random.uniform(-1, 1),
            "w4": random.uniform(-1, 1),
            "w5": random.uniform(-1, 1),
            "bias": random.uniform(-1, 1),
        }
    return weights


def Edit_Weights(Weights):
    Weights = copy.deepcopy(Weights)
    for Num in range(1, 11):
        for W in range(1, 6):
            Weights[Num][f"w{W}"] += random.uniform(-lr, lr)
        Weights[Num]["bias"] += random.uniform(-lr, lr)

    for i in range(1, 6):
        Weights[f"Speed_w{i}"] += random.uniform(-lr, lr)
        Weights[f"Angle_w{i}"] += random.uniform(-lr, lr)

    Weights["Speed_bias"] += random.uniform(-0.2, 0.2)
    Weights["Angle_bias"] += random.uniform(-0.2, 0.2)
    return Weights


File = Find_File()
Main_Weights = Get_File_Contents(File) if (TrainWithPreData or not TRAIN) else None
if Main_Weights is None:
    Main_Weights = Create_Random_Weights()


def Get_Outputs(Weights, Raycast1, Raycast2, Raycast3, Speed, Angle):
    Raycast1 = min(Raycast1 / 400, 1)
    Raycast2 = min(Raycast2 / 400, 1)
    Raycast3 = min(Raycast3 / 400, 1)
    Normalised_Angle = (Angle / 180) - 1

    Answers = {}
    Answers2 = {}

    for Neuron in range(1, 6):
        Ans = math.tanh(
            (Raycast1 * Weights[Neuron]["w1"])
            + (Raycast2 * Weights[Neuron]["w2"])
            + (Raycast3 * Weights[Neuron]["w3"])
            + (Speed * Weights[Neuron]["w4"])
            + (Normalised_Angle * Weights[Neuron]["w5"])
            + Weights[Neuron]["bias"]
        )
        Answers[f"Ans{Neuron}"] = Ans

    for Neuron in range(6, 11):
        Ans = math.tanh(
            (Answers["Ans1"] * Weights[Neuron]["w1"])
            + (Answers["Ans2"] * Weights[Neuron]["w2"])
            + (Answers["Ans3"] * Weights[Neuron]["w3"])
            + (Answers["Ans4"] * Weights[Neuron]["w4"])
            + (Answers["Ans5"] * Weights[Neuron]["w5"])
            + Weights[Neuron]["bias"]
        )
        Answers2[f"Ans{Neuron-5}"] = Ans

    Speed_Ans = (
        math.tanh(
            (Answers2["Ans1"] * Weights["Speed_w1"])
            + (Answers2["Ans2"] * Weights["Speed_w2"])
            + (Answers2["Ans3"] * Weights["Speed_w3"])
            + (Answers2["Ans4"] * Weights["Speed_w4"])
            + (Answers2["Ans5"] * Weights["Speed_w5"])
            + Weights["Speed_bias"]
        )
        + 1
    ) / 2

    Angle_Ans = (
        Angle
        + math.tanh(
            (Answers2["Ans1"] * Weights["Angle_w1"])
            + (Answers2["Ans2"] * Weights["Angle_w2"])
            + (Answers2["Ans3"] * Weights["Angle_w3"])
            + (Answers2["Ans4"] * Weights["Angle_w4"])
            + (Answers2["Ans5"] * Weights["Angle_w5"])
            + Weights["Angle_bias"]
        )
        * 45
    ) % 360

    return Speed_Ans, Angle_Ans


def Create_Clones(Starting_Weights, Num_Clones):
    global Training_Clones
    for i in range(Num_Clones - 1):
        Training_Clones[f"Clone{i+1}"] = Edit_Weights(Starting_Weights)
    Training_Clones[f"Clone{Num_Clones}"] = copy.deepcopy(Starting_Weights)


def Start_Race(Weight, Amount, RaceTime):
    global Training_Clones, Car_Info
    Training_Clones = {}
    Car_Info = {}
    Create_Clones(Weight, Amount)

    for Car in Training_Clones:
        Spawn_Car(Car)
        Car_Info[Car] = {"Alive": True, "Score": 0}

    Alive = len(Training_Clones)
    Runs = 0

    while Alive > 0 and Runs < RaceTime:
        Alive = 0
        for Car, car_weights in Training_Clones.items():
            if not Car_Info[Car]["Alive"]:
                continue

            Progress = Check_Progress(Car)
            if Progress["crashed"]:
                Car_Info[Car]["Alive"] = False
                Car_Info[Car]["Score"] = Progress["reward"]
                continue

            Alive += 1
            Info = Get_Info(Car)
            Speed, Angle = Get_Outputs(
                car_weights,
                Info["raycast1"],
                Info["raycast2"],
                Info["raycast3"],
                Info["speed"],
                Info["angle"],
            )
            Change_Value(Car, Speed, Angle)
            Car_Info[Car]["Score"] = Progress["reward"]

        Update()
        Render()
        Runs += 1

    for Car in Training_Clones:
        Car_Info[Car]["Score"] = Check_Progress(Car)["reward"]

    CarNum = max(Car_Info, key=lambda Car: Car_Info[Car]["Score"])
    print("Winner:", CarNum, "Score:", Car_Info[CarNum]["Score"])
    return Training_Clones[CarNum]


def Train(Repeats):
    global Main_Weights
    Start_GUI()
    Map = 0
    for i in range(Repeats):
        Map = (Map % 5) + 1
        Set_Map(Map)
        Main_Weights = Start_Race(Main_Weights, Clone_Per_Run, 900)
        Reset()
    Close_GUI()
    Write_File_Contents(Find_File(), Main_Weights)


def Test_Model():
    Start_GUI()
    Set_Map(1)
    Start_Race(Main_Weights, 1, 900)
    Reset()
    Close_GUI()





Train(20)
