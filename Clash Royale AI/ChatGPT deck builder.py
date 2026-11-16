import math
import ast
import hashlib
import itertools
try:
    import numpy as np
except ImportError as error:
    raise SystemExit('This builder requires NumPy. Install it with: python -m pip install numpy') from error
import random
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / 'Training_Data' / 'Clash_Royale.json'

random.seed(67)
def _load_training_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Training data not found: {DATA_FILE}")

    namespace = {}
    # The historical .json file contains Python literals, not JSON. Never execute it.
    tree = ast.parse(DATA_FILE.read_text(encoding='utf-8'))
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            raise ValueError("Training data must contain literal table assignments only")
        namespace[node.targets[0].id] = ast.literal_eval(node.value)

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

card_lookup = {card["Name"]: card for card in cards}
card_names = sorted(card_lookup)
card_indices = {name: i for i, name in enumerate(card_names)}
card_weights = None
model_report = {}

def _deck_cards(names):
    if len(names) != 8 or len(set(names)) != 8 or any(n not in card_lookup for n in names):
        raise ValueError("Enter 8 different valid card names")
    return [card_lookup[n] for n in names]


def calculate_average_attack_and_cost_and_defense(card_names):
    deck_cards = _deck_cards(card_names)
    if len(card_names) != 8 or len(set(card_names)) != 8 or len(deck_cards) != 8:
        raise ValueError("Enter 8 different valid card names")

    count = lambda key: sum(card[key] for card in deck_cards)
    win_conditions = count("WinCondition")
    buildings = count("Building")
    air = count("SustainedAir")
    ground = count("GroundDefense")
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
    defense = 0.7 + 0.22 * sum(strongest_defenders[:4]) + 0.25 * min(3, air) + 0.25 * min(2, anti_tank) + 0.18 * min(2, ground) - 0.3 * max(0, buildings - 2)

    if air == 0:
        defense -= 2.0
    if ground < 2:
        defense -= 0.75 * (2 - ground)
    return max(1, min(10, attack)), average_cost, max(1, min(10, defense))

def calculate_base_synergy_balance(card_names):
    deck_cards = _deck_cards(card_names)
    values = [sum(c[key] for c in deck_cards) for key in
              ("AirCounter", "GroundCounter", "Building", "SmallSpell", "BigSpell", "WinCondition")]
    # Keep using your independently trained model, without overwriting its weights.
    synergy = sum(globals()[f"s_w{i+1}"] * x for i, x in enumerate(values)) + s_bias
    balance = sum(globals()[f"b_w{i+1}"] * x for i, x in enumerate(values)) + b_bias
    return max(1, min(10, synergy)), max(1, min(10, balance))


def calculate_synergy_balance(card_names):
    if card_weights is None:
        return calculate_base_synergy_balance(card_names)
    return tuple(Deck_Values([card_names])[0][3:5])

TRAIN = False  # Set False after training to load this builder's own saved model.
# Training solves regularized squared error exactly; no noisy reward updates or epoch loop.
MODEL_VERSION = 1
MODEL_FILE = Path(__file__).resolve().parent / "Ai Models" / "Clash Royale" / "ChatGPT_Deck_Builder_Weights.json"
SEED = 67
SEARCH_ROUNDS = 5000
SEARCH_WIDTH = 8
TARGET_TOLERANCES = (1.0, 0.15, 1.0, 1.0, 1.0)  # attack, elixir, defense, synergy, balance
TARGET_IMPORTANCE = (1.0, 1.0, 1.0, 1.0, 1.0)
ROLE_KEYS = ("AirCounter", "GroundCounter", "Building", "SmallSpell", "BigSpell", "WinCondition",
             "Tank", "MiniTank", "Ranged", "Splash", "Swarm", "Support", "Reset", "AntiTank",
             "Spell", "DamageSpell", "SustainedAir", "GroundDefense", "Flying", "Champion", "Bait")

def Locate_Model(Name):
    filename = Name if Name.endswith(".json") else f"{Name}.json"
    exact = Path(__file__).resolve().parent / 'Ai Models' / 'Clash Royale' / filename
    if exact.exists():
        return exact
    
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        match = next(parent.glob(f"**/{filename}"), None)
        if match:
            return match

    match = next(Path.cwd().glob(f"**/{filename}"), None)
    if match:
        return match

    raise FileNotFoundError(f"Could not locate '{filename}' anywhere in the workspace.")


def Save_Card_Weights(name=None):
    # Separate artifact: never replace the original builder or synergy model.
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": MODEL_VERSION, "fingerprint": Data_Fingerprint(),
               "card_names": card_names, "coefficients": card_weights.tolist(),
               "report": model_report}
    temporary = MODEL_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(MODEL_FILE)
    print(f"Successfully saved card weights to: {MODEL_FILE}")


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
        value = float(saved[name])
        if not math.isfinite(value):
            raise ValueError(f'Non-finite saved parameter: {name}')
        globals()[name] = value


def Data_Fingerprint():
    baseline = [globals()[name] for name in MODEL_PARAMETERS]
    content = DATA_FILE.read_bytes() + json.dumps(baseline).encode() + repr(ROLE_KEYS).encode()
    return hashlib.sha256(content).hexdigest()


def Validate_Training_Data():
    if len(card_lookup) != len(cards):
        raise ValueError("Duplicate card names")
    for card in cards:
        if any(key not in card for key in ROLE_KEYS):
            raise ValueError(f"Missing role fields for {card['Name']}; update the training tables")
        if any(card[key] not in (0, 1) for key in ROLE_KEYS):
            raise ValueError(f"Role flags must be 0 or 1: {card['Name']}")
        if not all(math.isfinite(float(card[key])) for key in ('Cost', 'Attack', 'Defense')):
            raise ValueError("Non-finite card values")
    synergy_lookup = {}
    for row in synergy_data:
        _deck_cards(row['Cards'])
        key = tuple(sorted(row['Cards']))
        if key in synergy_lookup:
            raise ValueError("Duplicate synergy deck")
        if not all(1 <= row[k] <= 10 for k in ('Synergy', 'Balance')):
            raise ValueError("Synergy/balance labels must be 1-10")
        synergy_lookup[key] = row
    seen = set()
    for row in data:
        _deck_cards(row['Cards'])
        key = tuple(sorted(row['Cards']))
        if key in seen or key not in synergy_lookup:
            raise ValueError("Duplicate or unmatched training deck")
        if row['Name'] != synergy_lookup[key]['Name'] or not 1 <= row['target'] <= 10:
            raise ValueError("Mismatched training labels")
        seen.add(key)
    if seen != set(synergy_lookup):
        raise ValueError("The two training tables must describe the same decks")
    return synergy_lookup


def Deck_Features(names):
    deck = _deck_cards(names)
    attack, cost, defense = calculate_average_attack_and_cost_and_defense(names)
    base_syn, base_bal = calculate_base_synergy_balance(names)
    counts = {key: sum(c[key] for c in deck) for key in ROLE_KEYS}
    # Nonlinear role features distinguish coverage from redundant role stacking.
    roles = [counts[k] / 8 for k in ROLE_KEYS]
    structural = [
        float(counts['WinCondition'] == 0), float(counts['WinCondition'] == 1),
        float(counts['WinCondition'] == 2), max(0, counts['WinCondition'] - 2) / 6,
        float(counts['SustainedAir'] == 0), min(2, counts['SustainedAir']) / 2,
        float(counts['DamageSpell'] == 0), max(0, counts['Spell'] - 3) / 5,
        max(0, counts['Building'] - 2) / 6, min(2, counts['GroundDefense']) / 2,
        sum(c['Cost'] <= 2 for c in deck) / 8, sum(c['Cost'] >= 5 for c in deck) / 8,
        float(cost > 4.5), counts['Bait'] * counts['WinCondition'] / 16,
        counts['Tank'] * counts['Support'] / 16, counts['Splash'] * counts['Reset'] / 16,
        float(counts['Champion'] > 1),
    ]
    features = [1.0, attack / 10, cost / 10, defense / 10, base_syn / 10, base_bal / 10] + roles + structural
    identity = [0.0] * len(card_names)
    for name in names:
        identity[card_indices[name]] = 0.35
    # Stable signed hashing learns card-pair effects, not just role totals.
    pairs = [0.0] * 128
    for a, b in itertools.combinations(sorted(names), 2):
        digest = hashlib.blake2b((a + '\0' + b).encode(), digest_size=4).digest()
        value = int.from_bytes(digest, 'little')
        pairs[value % 128] += (1 if value & 128 else -1) / 7
    return features + identity + pairs


def _fit(features, labels, regularization):
    # Ridge regression is the exact minimizer of a deck-level squared-error objective.
    # Every card/pair receives credit according to its actual feature contribution.
    penalty = np.eye(features.shape[1]) * regularization
    penalty[0, 0] = 1e-8
    return np.linalg.solve(features.T @ features + penalty, features.T @ labels)


def Train_Card_Weights(Set_attack=None, Set_cost=None, Set_defense=None, Set_synergy=None, Set_balance=None):
    global card_weights, model_report
    synergy_lookup = Validate_Training_Data()
    groups = sorted({row['Name'].split(' / ')[0] for row in data},
                    key=lambda name: hashlib.sha256((str(SEED) + name).encode()).hexdigest())
    if len(groups) < 10:
        raise ValueError("At least ten independent deck groups are needed for evaluation")
    size = max(1, len(groups) // 5)
    test_groups, validation_groups = set(groups[:size]), set(groups[size:2 * size])
    features = np.asarray([Deck_Features(row['Cards']) for row in data], dtype=float)
    bases = np.asarray([calculate_base_synergy_balance(row['Cards']) for row in data])
    truth = np.asarray([[synergy_lookup[tuple(sorted(row['Cards']))]['Synergy'],
                         synergy_lookup[tuple(sorted(row['Cards']))]['Balance'], row['target']] for row in data])
    # Learn residuals around your supplied synergy/balance model, plus an overall rating.
    offsets = np.column_stack([bases, np.full(len(data), 5.0)])
    labels = (truth - offsets) / 10
    group_names = [row['Name'].split(' / ')[0] for row in data]
    test = np.asarray([g in test_groups for g in group_names])
    validation = np.asarray([g in validation_groups for g in group_names])
    train = ~(test | validation)
    best = None
    for regularization in (0.05, 0.5, 5.0):
        weights = _fit(features[train], labels[train], regularization)
        predicted = np.clip(offsets[validation] + 10 * (features[validation] @ weights), 1, 10)
        loss = float(np.mean((predicted - truth[validation]) ** 2))
        if best is None or loss < best[0]:
            best = (loss, regularization)
    # Test groups remain unseen; validation groups can now join the final fit.
    card_weights = _fit(features[~test], labels[~test], best[1])
    bounds = [truth[~test].min(axis=0).tolist(), truth[~test].max(axis=0).tolist()]
    predicted = np.clip(offsets[test] + 10 * (features[test] @ card_weights), *bounds)
    baseline = np.column_stack([bases[test], np.full(int(test.sum()), truth[~test, 2].mean())])
    model_report = {
        'label_source': 'Synthetic structural labels; these errors do not measure gameplay win rate.',
        'train_examples': int(train.sum()), 'validation_examples': int(validation.sum()),
        'test_examples': int(test.sum()), 'test_groups': sorted(test_groups),
        'validation_groups': sorted(validation_groups), 'regularization': best[1],
        'validation_mse': best[0], 'metric_order': ['synergy', 'balance', 'overall'],
        'test_mae': np.mean(np.abs(predicted - truth[test]), axis=0).tolist(),
        'baseline_test_mae': np.mean(np.abs(baseline - truth[test]), axis=0).tolist(),
        'label_bounds': bounds,
    }
    print('Held-out group MAE (synergy, balance, overall): ' + ', '.join(f'{v:.3f}' for v in model_report['test_mae']))
    print('Baseline MAE: ' + ', '.join(f'{v:.3f}' for v in model_report['baseline_test_mae']))
    print('Evaluation uses synthetic labels, not measured gameplay strength.')


def Load_Card_Weights():
    global card_weights, model_report
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"No saved ChatGPT builder model at {MODEL_FILE}; set TRAIN = True once")
    saved = json.loads(MODEL_FILE.read_text(encoding='utf-8'))
    if saved.get('version') != MODEL_VERSION or saved.get('fingerprint') != Data_Fingerprint() or saved.get('card_names') != card_names:
        raise ValueError('Saved ChatGPT builder model is stale; set TRAIN = True to retrain')
    weights = np.asarray(saved['coefficients'], dtype=float)
    if weights.shape != (len(Deck_Features(data[0]['Cards'])), 3) or not np.isfinite(weights).all():
        raise ValueError('Invalid saved ChatGPT builder weights')
    card_weights, model_report = weights, saved['report']


def Deck_Values(decks):
    if card_weights is None:
        raise ValueError('Train or load the ChatGPT builder before evaluating decks')
    features = np.asarray([Deck_Features(deck) for deck in decks])
    corrections = features @ card_weights * 10
    values = []
    for deck, correction in zip(decks, corrections):
        attack, cost, defense = calculate_average_attack_and_cost_and_defense(deck)
        syn, bal = calculate_base_synergy_balance(deck)
        # Search must not exploit extrapolated 10/10 scores unsupported by training labels.
        learned = np.clip(np.asarray([syn, bal, 5.0]) + correction, *model_report['label_bounds'])
        values.append([attack, cost, defense, *learned])
    return np.asarray(values)


def Proper_Deck(names):
    deck = _deck_cards(names)
    count = lambda key: sum(c[key] for c in deck)
    # Enforce composition before optimizing the requested settings.
    return (1 <= count('WinCondition') <= 2 and count('Champion') <= 1
            and count('SustainedAir') >= 1 and count('GroundDefense') >= 2
            and count('DamageSpell') >= 1 and count('Building') <= 2
            and count('Spell') <= 4 and 'Mirror' not in names)


def Target_Loss(values, targets):
    errors = (values[:, :5] - np.asarray(targets)) / np.asarray(TARGET_TOLERANCES)
    # Squared distance penalizes overshooting and undershooting equally.
    return np.mean(errors ** 2 * np.asarray(TARGET_IMPORTANCE), axis=1)


def Use_Deck_Model(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance):
    global last_search_report
    targets = (Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance)
    if not all(math.isfinite(float(v)) for v in targets):
        raise ValueError('Targets must be finite numbers')
    if any(not 1 <= v <= 10 for i, v in enumerate(targets) if i != 1) or not 1 <= Set_cost <= 9:
        raise ValueError('Ratings must be 1-10 and average elixir must be 1-9')
    if any(v <= 0 for v in TARGET_TOLERANCES) or any(v < 0 for v in TARGET_IMPORTANCE) or not any(TARGET_IMPORTANCE):
        raise ValueError('Tolerances must be positive and importance weights nonnegative, with at least one positive')
    if TRAIN:
        Train_Card_Weights(*targets)
    elif card_weights is None:
        Load_Card_Weights()
    # Exclude held-out groups even from search seeds and pair-based retrieval.
    training_rows = [row for row in data if row['Name'].split(' / ')[0] not in model_report['test_groups']]
    positive_rows = [row for row in training_rows if row['target'] >= 7]
    eligible = sorted({n for row in positive_rows for n in row['Cards']} - {'Mirror'})
    candidates = sorted({tuple(sorted(row['Cards'])) for row in positive_rows if Proper_Deck(row['Cards'])})
    if not candidates:
        raise ValueError('No valid seed decks satisfy the composition rules')
    evaluated = set()
    def rank(decks):
        values = Deck_Values(decks)
        loss = Target_Loss(values, targets)
        # All five settings drive selection; rating only breaks near-equal target fits.
        objective = loss + 0.08 * ((10 - values[:, 5]) / 9) ** 2
        order = np.argsort(objective, kind='stable')
        return [(float(objective[i]), tuple(decks[i]), values[i]) for i in order]
    ranked = rank(candidates)
    evaluated.update(candidates)
    best = ranked[0]
    beam = ranked[:SEARCH_WIDTH]
    for step in range(SEARCH_ROUNDS):
        neighbors = set()
        for _, deck, _ in beam:
            for index in range(8):
                for name in eligible:
                    if name in deck:
                        continue
                    changed = tuple(sorted(deck[:index] + (name,) + deck[index+1:]))
                    if changed not in evaluated and Proper_Deck(changed):
                        neighbors.add(changed)
        if not neighbors:
            break
        evaluated.update(neighbors)
        ranked = rank(sorted(neighbors))
        combined = sorted(beam + ranked[:SEARCH_WIDTH], key=lambda item: (item[0], item[1]))
        next_beam = combined[:SEARCH_WIDTH]
        if next_beam[0][0] < best[0]:
            best = next_beam[0]
        if [item[1] for item in beam] == [item[1] for item in next_beam]:
            break
        beam = next_beam
    last_search_report = {'targets': targets, 'values': best[2].tolist(), 'evaluated': len(evaluated),
                          'within_tolerance': (np.abs(best[2][:5] - targets) <= TARGET_TOLERANCES).tolist()}
    return list(best[1])


def Print_Values(Deck):
    values = Deck_Values([Deck])[0]
    print('Chosen Deck:')
    print('\n'.join(Deck))
    print()
    for label, value in zip(('Attack', 'Cost', 'Defense', 'Synergy', 'Balance', 'Overall rating'), values):
        suffix = ' elixir' if label == 'Cost' else '/10'
        print(f'{label}: {value:.2f}{suffix}')
    print('Overall rating estimates structural quality, not a win probability.')
    if last_search_report:
        print(f"Searched {last_search_report['evaluated']} complete decks.")
        for i, label in enumerate(('Attack', 'Cost', 'Defense', 'Synergy', 'Balance')):
            target = last_search_report['targets'][i]
            print(f'{label} target: {target:g}; difference: {values[i] - target:+.2f}')
        if not all(last_search_report['within_tolerance']):
            print('Some targets remain outside tolerance. This is the closest deck found by the search, not a guaranteed global optimum.')
        for column, name, target_index in ((0, 'Synergy', 3), (1, 'Balance', 4)):
            low, high = (bound[column] for bound in model_report['label_bounds'])
            if not low <= last_search_report['targets'][target_index] <= high:
                print(f'{name} target is outside the learned label range ({low:g}-{high:g}); scores are capped to that range.')
        if abs(last_search_report['targets'][1] * 8 - round(last_search_report['targets'][1] * 8)) > 1e-8:
            print('Exact average elixir is limited to steps of 0.125 for eight fixed-cost cards.')


AttackRating = 8
DefenceRating = 9.5
CostRating = 2.7
SynergyRating = 10
BalanceRating = 10
last_search_report = {}


def main():
    Validate_Training_Data()
    Load_Model(Locate_Model('Balance_And_Synergy.json'), MODEL_PARAMETERS)
    chosen_deck = Use_Deck_Model(AttackRating, CostRating, DefenceRating, SynergyRating, BalanceRating)
    Print_Values(chosen_deck)
    if TRAIN:
        Save_Card_Weights()


if __name__ == '__main__':
    main()
    

