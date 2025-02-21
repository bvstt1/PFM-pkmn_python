import random
from pprint import pprint
from pokeload import get_all_pokemon, get_pokemon


def get_player_profile(pokemon_list):
    return {
        "player name": input("¿Cual es tu nombre?: "),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }

def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print("Elige con que pokemon lucharás")
        for index in range(len(player_profile["pokemon_inventory"])):
            print(f"{index} - {get_pokemon_info(player_profile['pokemon_inventory'][index])}")
        try:
            return player_profile['pokemon_inventory'][int(input("¿Cual eliges?: "))]
        except (ValueError, IndexError):
            print("Opción invalida")



def get_pokemon_info(pokemon):
    return f"{pokemon['name']} | lvl {pokemon['level']} | hp {pokemon['current_health']} / {pokemon['base_health']}"

def fight(player_profile, enemy_pokemon):
    print ("---NUEVO COMBATE---")
    player_pokemon = choose_pokemon(player_profile)
    print(f"Contrincantes: {get_pokemon_info(player_pokemon)} VS {get_pokemon_info(enemy_pokemon)}")

    while any_player_pokemon_lives(player_profile) and enemy_pokemon['current_health'] > 0:
    player_attack(player_pokemon, enemy_pokemon)
    enemy_attack(enemy_pokemon, player_pokemon)

    print("--FIN DEL COMBATE--")
    input("Presiona ENTER para continuar...")


def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)


    print(f"Has perdido en el combate numero: {player_profile['combats']}")


if __name__ ==  "__main__":
    main()