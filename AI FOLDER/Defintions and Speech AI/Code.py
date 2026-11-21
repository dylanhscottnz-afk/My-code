from pathlib import Path
import json
import math
import random


def Find_File(Name):
  workspace = Path(".")
  AllJsonFiles = list(workspace.rglob("*.json"))
  for File in AllJsonFiles:
    if File.name == Name:
      return File
  return None


def Load_File(Name):
  with open(Name, "r", encoding="utf-8") as file:
    data = json.load(file)
  return {int(k) if k.isdigit() else k: v for k, v in data.items()}

def Write_File_Contents(file_path, info):
    if file_path is None:
        print("Cannot save: no file path provided.")
        return
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4)



Abc = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
    " ": 27,
    ".": 28,
    ",": 29,
    "!": 30,
    "?": 31,
    "'": 32,
    "-": 33,
    ":": 34,
    ";": 35,
    "(": 36,
    ")": 37,
}


Speech_To_Num = {
    "Noun":	1,
    "Verb":	2,
    "Adjective":	3,
    "Adverb":	4,
    "Pronoun":	5,
    "Preposition":	6
}

Data = Load_File(Find_File("Def_And_Speech_Training_Data.json"))

TRAIN = True
Letters = {}
Type_Of_Speech_Weights = {}
Epochs = 50
lr = 0.0001
Ans_table_1 = []
AI_Model_Name = "Def_And_Speech_AI.json"

def Get_Token(Letter):
  return Abc.get(Letter.lower(), 0)

def Tokenise_String(Str):
  Tokens = []
  for L in range(len(Str)):
    token_val = Get_Token(Str[L])
    if token_val > 0:
      Tokens.append(token_val / 37)
    else:
      Tokens.append(0)
    
  for i in range(10 - len(Tokens)):
    Tokens.append(0)
  return Tokens

def Get_Speech_From_Num(Num):
  for i in Speech_To_Num:
    if Speech_To_Num[i] == Num:
      return i
  return "No Speech type"

for W in Data:
  Letters[W] = Tokenise_String(W)

def Train():
  global Type_Of_Speech_Weights

  def Type_Of_Speech_AI():
    
    for w2 in range(1, 6):
      Type_Of_Speech_Weights[f"N{w2}"] = {}
      for w in range(1, 11):
        Type_Of_Speech_Weights[f"N{w2}"][f"w{w}"] = random.uniform(-1, 1)
      Type_Of_Speech_Weights[f"N{w2}"]["bias"] = random.uniform(-1, 1)
    for i in range(1, 6):
      Type_Of_Speech_Weights[f"w{i}"] = random.uniform(-1, 1)
    Type_Of_Speech_Weights["bias"] = random.uniform(-1, 1)
      
      
    for epoch in range(Epochs):
      for Word in Data:
        Letter_Table = Tokenise_String(Word)
        Target = Speech_To_Num[Data[Word]["Speech"]]
        Ans_table_1 = []
        for w in range(1, 6):

          
          Ans_table_1.append(math.tanh(
              (Letter_Table[0] * Type_Of_Speech_Weights[f"N{w}"][f"w1"]) +
              (Letter_Table[1] * Type_Of_Speech_Weights[f"N{w}"][f"w2"]) +
              (Letter_Table[2] * Type_Of_Speech_Weights[f"N{w}"][f"w3"]) +
              (Letter_Table[3] * Type_Of_Speech_Weights[f"N{w}"][f"w4"]) +
              (Letter_Table[4] * Type_Of_Speech_Weights[f"N{w}"][f"w5"]) +
              (Letter_Table[5] * Type_Of_Speech_Weights[f"N{w}"][f"w6"]) +
              (Letter_Table[6] * Type_Of_Speech_Weights[f"N{w}"][f"w7"]) +
              (Letter_Table[7] * Type_Of_Speech_Weights[f"N{w}"][f"w8"]) +
              (Letter_Table[8] * Type_Of_Speech_Weights[f"N{w}"][f"w9"]) +
              (Letter_Table[9] * Type_Of_Speech_Weights[f"N{w}"][f"w10"]) +
              Type_Of_Speech_Weights[f"N{w}"]["bias"]
          ))
        
        z = (
            Ans_table_1[0] * Type_Of_Speech_Weights["w1"] +
            Ans_table_1[1] * Type_Of_Speech_Weights["w2"] +
            Ans_table_1[2] * Type_Of_Speech_Weights["w3"] +
            Ans_table_1[3] * Type_Of_Speech_Weights["w4"] +
            Ans_table_1[4] * Type_Of_Speech_Weights["w5"] +
            Type_Of_Speech_Weights["bias"]
        )

        FinalAns = (math.tanh(z) + 1) * 2.5 + 1
        Error = FinalAns - Target
        Gradient = Error * 2.5 * (1 - math.tanh(z) ** 2)
        
        for l in range(1, 6):
          HiddenGradient = Gradient * Type_Of_Speech_Weights[f"w{l}"] * (1 - Ans_table_1[l-1] ** 2)
          for i in range(1, 11):
            Type_Of_Speech_Weights[f"N{l}"][f"w{i}"] -= HiddenGradient * lr * Letter_Table[i-1]
          Type_Of_Speech_Weights[f"N{l}"]["bias"] -= HiddenGradient * lr
          Type_Of_Speech_Weights[f"w{l}"] -= Gradient * lr * Ans_table_1[l-1]
        Type_Of_Speech_Weights[f"bias"] -= Gradient * lr
          
  Type_Of_Speech_AI()
  Write_File_Contents(Find_File(AI_Model_Name) or AI_Model_Name, Type_Of_Speech_Weights)
def Test_Type_Of_Speech(Word):
  Letter_Table = Tokenise_String(Word)
  Ans_table_1 = []
  for w in range(1, 6):
    Ans_table_1.append(math.tanh(
        (Letter_Table[0] * Type_Of_Speech_Weights[f"N{w}"][f"w1"]) +
        (Letter_Table[1] * Type_Of_Speech_Weights[f"N{w}"][f"w2"]) +
        (Letter_Table[2] * Type_Of_Speech_Weights[f"N{w}"][f"w3"]) +
        (Letter_Table[3] * Type_Of_Speech_Weights[f"N{w}"][f"w4"]) +
        (Letter_Table[4] * Type_Of_Speech_Weights[f"N{w}"][f"w5"]) +
        (Letter_Table[5] * Type_Of_Speech_Weights[f"N{w}"][f"w6"]) +
        (Letter_Table[6] * Type_Of_Speech_Weights[f"N{w}"][f"w7"]) +
        (Letter_Table[7] * Type_Of_Speech_Weights[f"N{w}"][f"w8"]) +
        (Letter_Table[8] * Type_Of_Speech_Weights[f"N{w}"][f"w9"]) +
        (Letter_Table[9] * Type_Of_Speech_Weights[f"N{w}"][f"w10"]) +
        Type_Of_Speech_Weights[f"N{w}"]["bias"]
    ))
    
  z = (
    Ans_table_1[0] * Type_Of_Speech_Weights["w1"] +
    Ans_table_1[1] * Type_Of_Speech_Weights["w2"] +
    Ans_table_1[2] * Type_Of_Speech_Weights["w3"] +
    Ans_table_1[3] * Type_Of_Speech_Weights["w4"] +
    Ans_table_1[4] * Type_Of_Speech_Weights["w5"] +
    Type_Of_Speech_Weights["bias"]
  )
  FinalAns = (math.tanh(z) + 1) * 2.5 + 1
  
  
  
  return Get_Speech_From_Num(round(FinalAns))

if TRAIN:
  Train()
else:
  Type_Of_Speech_Weights = Load_File(Find_File(AI_Model_Name))

print(Test_Type_Of_Speech("Lantern"))
