import json
import time
import random
import datetime
import os



time_date = datetime.datetime.now()
random.seed(int(time_date.strftime('%Y%m%d%H%M%S%f')))
deck_filename = f"deck_{time_date.strftime('%Y%m%d%H%M%S%f')}.txt"
spacer_char = " "
MIN_LANDS = 30
MAX_TRYS = 10000

# Must equal 1.0
DefaultDeckWeights = {
    "Basic": 0.50,
    "Land": 0.45,
    "Creature": 0.20,
    "Enchantment": 0.10,
    "Artifact": 0.10,
    "Planeswalker": 0.02,
    "Instant": 0.08,
    "Sorcery": 0.05
}

# LandTable = {
#     "W": "Plains",
#     "U": "Island",
#     "B": "Swamp",
#     "R": "Mountain",
#     "G": "Forest"
# }

LandTable = {
    "W": 0,
    "U": 1,
    "B": 2,
    "R": 3,
    "G": 4
}


if not(os.path.exists('AllPrintings.json')):
    print("Download 'AllPrintings.json' from 'https://mtgjson.com/downloads/all-files/' and place in the same directory as this program.")
    
    while not(os.path.exists('AllPrintings.json')):
        time.sleep(1)

if os.path.exists('DeckWeights.json'):
    with open('DeckWeights.json', 'r') as f:
        DeckWeights = json.load(f)
else:
    with open('DeckWeights.json', 'w') as f:
        json.dump(DefaultDeckWeights, f, indent=4)
    DeckWeights = DefaultDeckWeights

if not(os.path.isdir("decks")):
    os.mkdir("decks")
    
    


print("loading json")
start_time = time.time()

with open('AllPrintings.json', 'r', encoding='utf-8') as f:
    MTG_Database = json.load(f)

print(f"finished json loading in {(time.time() - start_time):.1f}s")
print(f"MTGJson version {MTG_Database['meta']['version']}")
#print(MTG_Database)

# for card in MTG_Database['data']['M14']['cards']:
#     print(f"{card['name']} {card['colorIdentity']} {len(card['colorIdentity'])} {card['types']}")
#     if card['colorIdentity'] == None:
#         print("NONE")


# print(MTG_Database['data'][0])
# print(MTG_Database['meta'])

mtg_sets = list(MTG_Database['data'].keys())
ii = 0
start_time = time.time()
while True:
    mtg_set = random.choice(mtg_sets)
    #print(f"{ii} set={set}")
    ii = ii + 1
    cards = MTG_Database['data'][mtg_set]['cards']
    if len(cards) < 1:
        continue
    commander = random.choice(cards)
    
    if ('Legendary' in commander['supertypes']):
        if ('Creature' in commander['types']):
            try:
                if ('Legal' in commander['legalities']['commander']):
                    print(f"commander found in {ii} trys, taking {(time.time() - start_time):.1f}s")
                    break
            except KeyError:
                continue


colorIdentity = commander['colorIdentity']
print(f"{commander['name']}, {colorIdentity}")
deck_list = []
deck_list.append(str(commander['name']))


total_cards = 1
types = list(DeckWeights.keys())
types.pop(0)
weights = list(DeckWeights.values())
basic = weights.pop(0)
#WUBGR WASTES
basic_lands = [0,0,0,0,0,0]

while total_cards < 100:
    card_type = random.choices(types,weights=weights, k=1)
    if card_type[0] == 'Land':
        if random.random() <= basic:
            if len(colorIdentity) > 0:
                card = random.choice(colorIdentity)
                basic_lands[LandTable[card]] += 1
            else:
                basic_lands[5] += 1
            total_cards += 1
            continue



    ii = 0
    while True:
        mtg_set = random.choice(mtg_sets)
        cards = MTG_Database['data'][mtg_set]['cards']
        if len(cards) < 1:
            continue

        card = random.choice(cards)

        dummy = []
        dummy.append(str(card['name']))
        common_cards = set(dummy) & set(deck_list)

        if len(common_cards) == 0:
            if (card_type[0] in card['types']):
                uncommon_colors = list(set(card['colorIdentity']) - set(colorIdentity))
                if len(uncommon_colors) == 0:
                    try:
                        if ('Legal' in card['legalities']['commander']):
                            deck_list.append(str(card['name']))
                            total_cards += 1
                            break
                    except KeyError:
                        continue
        
        ii += 1
        if ii > MAX_TRYS:
            print("FUCK")
            break


with open("decks/" + deck_filename, "w") as f:

    for card in deck_list:
        f.write(f"1{spacer_char}{card}\n")
    
    if basic_lands[0] > 0:
        f.write(f"{basic_lands[0]}{spacer_char}Plains\n")

    if basic_lands[1] > 0:
        f.write(f"{basic_lands[1]}{spacer_char}Island\n")

    if basic_lands[2] > 0:
        f.write(f"{basic_lands[2]}{spacer_char}Swamp\n")

    if basic_lands[3] > 0:
        f.write(f"{basic_lands[3]}{spacer_char}Mountain\n")

    if basic_lands[4] > 0:
        f.write(f"{basic_lands[4]}{spacer_char}Forest\n")

    if basic_lands[5] > 0:
        f.write(f"{basic_lands[5]}{spacer_char}Wastes\n")

print(f"Finished Deck in {(time.time() - start_time):.3f}s")












#a['data']['2ED']['cards'][0].keys()
#dict_keys(['artist', 'artistIds', 'availability', 'boosterTypes', 'borderColor', 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'edhrecSaltiness', 'finishes', 'foreignData', 'frameVersion', 'identifiers', 'isReprint', 'keywords', 'language', 'layout', 'legalities', 'manaCost', 'manaValue', 'name', 'number', 'originalText', 'printings', 'purchaseUrls', 'rarity', 'rulings', 'setCode', 'sourceProducts', 'subtypes', 'supertypes', 'text', 'type', 'types', 'uuid'])

# >>> a['data']['M14'].keys()
# dict_keys(['baseSetSize', 'block', 'booster', 'cards', 'code', 'decks', 'isFoilOnly', 'isOnlineOnly', 'keyruneCode', 'languages', 'mcmId', 'mcmName', 'mtgoCode', 'name', 'releaseDate', 'sealedProduct', 'tcgplayerGroupId', 'tokenSetCode', 'tokens', 'totalSetSize', 'translations', 'type'])