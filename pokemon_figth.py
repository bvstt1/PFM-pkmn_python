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

def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def fight():
    pass


def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)


    print(f"Has perdido en el combate numero: {player_profile["combats"]}")


if __name__ ==  "__main__":
    main()