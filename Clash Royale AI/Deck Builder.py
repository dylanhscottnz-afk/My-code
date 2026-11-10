import math
import random
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / 'Training_Data' / 'Clash_Royale.json'

random.seed(67)
def _load_training_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Training data not found: {DATA_FILE}")

    namespace = {}
    with DATA_FILE.open('r', encoding='utf-8') as handle:
        exec(handle.read(), namespace, namespace)

    cards = namespace.get('cards')
    data = namespace.get('data')
    synergy_data = namespace.get('synergy_data')

    if not cards:
        raise ValueError(f"No card data found in {DATA_FILE}")
    if not data:
        raise ValueError(f"No deck training data found in {DATA_FILE}")
    if synergy_data is None:
        synergy_data = data

    return cards, data, synergy_data


cards, data, synergy_data = _load_training_data()

card_weights = {
    card["Name"]: {
        "w_attack":  random.uniform(-0.1, 0.1),
        "w_cost":    random.uniform(-0.1, 0.1),
        "w_defense": random.uniform(-0.1, 0.1),
        "w_synergy": random.uniform(-0.1, 0.1),
        "w_balance": random.uniform(-0.1, 0.1),
        "bias":      0.0
    }
    for card in cards
}


def calculate_average_attack_and_cost_and_defense(card_names):
    deck_cards = [card for card in cards if card["Name"] in card_names]
    if len(card_names) != 8 or len(set(card_names)) != 8 or len(deck_cards) != 8:
        raise ValueError("Enter 8 different valid card names")

    count = lambda key: sum(card[key] for card in deck_cards)
    win_conditions = count("WinCondition")
    buildings = count("Building")
    air = count("AirCounter")
    ground = count("GroundCounter")
    anti_tank = count("AntiTank")
    total_cost = sum(card["Cost"] for card in deck_cards)
    average_cost = total_cost / 8

    main_attack = max((card["Attack"] for card in deck_cards if card["WinCondition"]), default=0)
    support_attack = sum(card["Attack"] for card in deck_cards if not card["WinCondition"]) / 7
    spell_attack = sum(card["Attack"] for card in deck_cards if card["SmallSpell"] or card["BigSpell"])
    attack = 0.7 + 0.69 * main_attack + 0.15 * min(8, support_attack) + 0.11 * spell_attack - 0.35 * max(0, win_conditions - 2)
    if win_conditions == 0:
        attack = min(attack, 3.0)

    strongest_defenders = sorted((card["Defense"] for card in deck_cards), reverse=True)
    defense = 0.7 + 0.29 * sum(strongest_defenders[:4]) + 0.25 * min(3, air) + 0.25 * min(2, anti_tank) + 0.18 * min(2, ground) - 0.3 * max(0, buildings - 2)

    return max(1, min(10, attack)), average_cost, max(1, min(10, defense))

def calculate_synergy_balance(card_names):
    deck_cards = [
        card for card in cards
        if card["Name"] in card_names
    ]

    if len(card_names) != 8 or len(set(card_names)) != 8 or len(deck_cards) != 8:
        raise ValueError("Enter 8 different valid card names")

    x1 = sum(card["AirCounter"] for card in deck_cards)
    x2 = sum(card["GroundCounter"] for card in deck_cards)
    x3 = sum(card["Building"] for card in deck_cards)
    x4 = sum(card["SmallSpell"] for card in deck_cards)
    x5 = sum(card["BigSpell"] for card in deck_cards)
    x6 = sum(card["WinCondition"] for card in deck_cards)

    synergy = (
        s_w1*x1 + s_w2*x2 + s_w3*x3 +
        s_w4*x4 + s_w5*x5 + s_w6*x6 + s_bias
    )

    balance = (
        b_w1*x1 + b_w2*x2 + b_w3*x3 +
        b_w4*x4 + b_w5*x5 + b_w6*x6 + b_bias
    )

    return (
        round(max(1, min(10, synergy)), 2),
        round(max(1, min(10, balance)), 2)
    )

TRAIN = True
epochs = 1000
lr = 0.01

def Locate_Model(Name):
    filename = Name if Name.endswith(".json") else f"{Name}.json"
    
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        match = next(parent.glob(f"**/{filename}"), None)
        if match:
            return match

    match = next(Path.cwd().glob(f"**/{filename}"), None)
    if match:
        return match

    raise FileNotFoundError(f"Could not locate '{filename}' anywhere in the workspace.")


def Save_Card_Weights(name):
    filename = name if name.endswith(".json") else f"{name}.json"
    
    try:
        model_ref = Locate_Model("Balance_And_Synergy.json")
        target_path = model_ref.parent / filename
    except FileNotFoundError:
        target_path = Path(__file__).resolve().parent / filename

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(card_weights, f, indent=2)

    print(f"Successfully saved card weights to: {target_path}")




MODEL_PARAMETERS = (
    "s_w1", "s_w2", "s_w3", "s_w4", "s_w5", "s_w6", "s_bias",
    "b_w1", "b_w2", "b_w3", "b_w4", "b_w5", "b_w6", "b_bias")

Parameters2 = ("w_attack", "w_cost", "w_defense", "w_synergy", "w_balance", "bias")
Parameters3 = ("cards", "data", "synergy_data")

def Load_Model(ModelFile, Parameters):
    
    if not ModelFile.exists():
        raise FileNotFoundError(
            f"No saved model at {ModelFile}. Set TRAIN = True and run once first."
        )
    saved = json.loads(ModelFile.read_text(encoding="utf-8"))
    missing = [name for name in Parameters if name not in saved]
    if missing:
        raise ValueError(f"Saved model is missing parameters: {missing}")
    for name in Parameters:
        globals()[name] = float(saved[name])
    

Load_Model(Locate_Model("Balance_And_Synergy.json"), MODEL_PARAMETERS)

w_attack = random.uniform(-1, 1)
w_cost = random.uniform(-1, 1)
w_defense = random.uniform(-1, 1)
w_synergy = random.uniform(-1, 1)
w_balance = random.uniform(-1, 1)
bias = random.uniform(-1, 1)
def Train_Card_Weights(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance):
    all_card_names = [card["Name"] for card in cards]

    for epoch in range(epochs):
        scores = {}
        for name in all_card_names:
            w = card_weights[name]
            score = (
                (Set_attack  * w["w_attack"])  +
                (Set_cost    * w["w_cost"])    +
                (Set_defense * w["w_defense"]) +
                (Set_synergy * w["w_synergy"]) +
                (Set_balance * w["w_balance"]) +
                w["bias"]
            )
            scores[name] = score + random.uniform(-1.0, 1.0)

        chosen_deck = sorted(scores, key=scores.get, reverse=True)[:8]

        att, cost, df = calculate_average_attack_and_cost_and_defense(chosen_deck)
        syn, bal = calculate_synergy_balance(chosen_deck)

        err_attack  = att - Set_attack
        err_cost    = cost - Set_cost
        err_defense = df - Set_defense
        err_synergy = syn - Set_synergy
        err_balance = bal - Set_balance

        reward_by_metric = {
            "w_attack": -err_attack,
            "w_cost": -err_cost,
            "w_defense": -err_defense,
            "w_synergy": -err_synergy,
            "w_balance": -err_balance,
        }

        for name in chosen_deck:
            w = card_weights[name]
            w["w_attack"]  += lr * reward_by_metric["w_attack"]  * 0.05
            w["w_cost"]    += lr * reward_by_metric["w_cost"]    * 0.05
            w["w_defense"] += lr * reward_by_metric["w_defense"] * 0.05
            w["w_synergy"] += lr * reward_by_metric["w_synergy"] * 0.05
            w["w_balance"] += lr * reward_by_metric["w_balance"] * 0.05
            w["bias"]      += lr * (
                reward_by_metric["w_attack"] +
                reward_by_metric["w_cost"] +
                reward_by_metric["w_defense"] +
                reward_by_metric["w_synergy"] +
                reward_by_metric["w_balance"]
            ) * 0.01




def Use_Deck_Model(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance):
    if TRAIN:
        Train_Card_Weights(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance)

    all_card_names = [card["Name"] for card in cards]
    final_scores = {}

    for name in all_card_names:
        w = card_weights[name]
        final_scores[name] = (
            (Set_attack  * w["w_attack"])  +
            (Set_cost    * w["w_cost"])    +
            (Set_defense * w["w_defense"]) +
            (Set_synergy * w["w_synergy"]) +
            (Set_balance * w["w_balance"]) +
            w["bias"]
        )

    return sorted(final_scores, key=final_scores.get, reverse=True)[:8]

def Print_Values(Deck):
    AttackResult, CostResult, DefenceResult = calculate_average_attack_and_cost_and_defense(Deck)
    SynergyResult, BalanceResult = calculate_synergy_balance(Deck)

    print(f"Attack: {AttackResult}")
    print(f"Cost: {CostResult}")
    print(f"Defense: {DefenceResult}")
    print(f"Synergy: {SynergyResult}")
    print(f"Balance: {BalanceResult}")

AttackRating = 5
DefenceRating = 10
CostRating = 2.7
SynergyRating = 10
BalanceRating = 10

chosen_deck = Use_Deck_Model(AttackRating, CostRating, DefenceRating, SynergyRating, BalanceRating)
print(f"Chosen Deck: {chosen_deck}")
Print_Values(chosen_deck)

if TRAIN:
    Save_Card_Weights("Deck_Builder_Weights.json")