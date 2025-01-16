import random
from pprint import pprint

from pokeload import get_all_pokemon


def get_player_profile(pokemon_list):
    return {
        "player name": input("¿Cual es tu nombre?: "),
        "pokemon_iventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }

def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile(pokemon_list)
    pprint(player_profile)

if __name__ ==  "__main__":
    main()