import random
import os
import time
from pokeload import get_all_pokemon, get_pokemon

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_player_profile():
    return {
        "player name": input("¿Cual es tu nombre?: "),
        "pokemon_inventory": [],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }

def inventory_menu(player_profile):
    while True:
        try:
            clear_screen()
            option = int(input('''+--------------------------------------------------+
|                    Inventario                    |
+--------------------------------------------------+
| 1) Datos                                         |
| 2) Objetos                                       |
| 3) Equipo pokemon                                |
| 4) Salir                                         |
+--------------------------------------------------+
Elija una opción: '''))

            if option == 1:
                clear_screen()
                input(f'''+--------------------------------------------------+
|                    Inventario                    |
+--------------------------------------------------+
 Nombre: {player_profile['player name']}         
 Combates: {player_profile['combats']}            
+--------------------------------------------------+
Presione ENTER para volver al menu de inventario... ''')

            elif option == 2:
                clear_screen()
                input(f'''+--------------------------------------------------+
|                    Inventario                    |
+--------------------------------------------------+
 Pokebolas: {player_profile['pokeballs']}
 Pociones: {player_profile['health_potion']}         
+--------------------------------------------------+
Presione ENTER para volver al menu de inventario... ''')

            elif option == 3:
                clear_screen()
                print('''+--------------------------------------------------+
|                    Inventario                    |
+--------------------------------------------------+''')
                stats = [(pokemon["name"], pokemon["level"], pokemon["base_health"], pokemon["base_health"],
                          pokemon["attack"], pokemon["defense"], pokemon["speed"])
                         for pokemon  in player_profile["pokemon_inventory"]]
                for cont, (name, level, base_healt, base_health, attack, defense, speed)  in enumerate(stats, start=1):
                    print(f" {cont}) {name} | Nivel: {level} | Salud: {base_health}/{base_healt} | Ataque: {attack} | "
                          f"Defensa: {defense} | Velocidad: {speed}")

                int(input('''+--------------------------------------------------+
Presione ENTER para volver al menú de inventario... '''))


            elif option == 4:
                clear_screen()
                print("Saliendo del inventario...")
                time.sleep(1)
                break

            else:
                print("Opción no válida. Por favor, elija entre 1, 2, 3 o 4.")

        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")
            time.sleep(2)
    return


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def attacks_pokemon(pokemon):
    return [attack for attack in pokemon["attacks"] if attack["min level"] <= pokemon["level"]]

def choosen_pkmn(random_pokemon, player_profile, option):
    chosen_pokemon = random_pokemon[option - 1]
    chosen_pokemon["level"] = 5
    chosen_pokemon['attacks'] = attacks_pokemon(chosen_pokemon)
    player_profile['pokemon_inventory'].append(chosen_pokemon)
    return chosen_pokemon

def choose_pokemon(pokemon_list, player_profile):
    chosen = None
    random_pokemon = random.sample(pokemon_list, 3)
    names_pkmn = [pkm["name"] for pkm in random_pokemon]
    while not chosen:
        print("Elige uno de estos 3 Pokemon que te ha dejado el Profesor Elias")
        for cont, nombres in enumerate(names_pkmn, start = 1):
            print(cont, nombres)
        try:
            option = int(input("¿Cual eliges?: "))
            if option == 1:
                return choosen_pkmn(random_pokemon, player_profile, option)
            elif option == 2:
                return choosen_pkmn(random_pokemon, player_profile, option)
            elif option == 3:
                return choosen_pkmn(random_pokemon, player_profile, option)

        except (ValueError, IndexError):
            print("Opción invalida")
    return

def get_enemy_profile():
    return {
        "pokemon_inventory": [],
        "health_potion": 0,
    }

def get_choose_player_pokemon_fight(player_profile):
    names_pkmn = [pokemon["name"] for pokemon in player_profile["pokemon_inventory"]]
    print ("¿Que Pokémon quieres elegir?")
    for cont, nombres in enumerate(names_pkmn, start=1):
        print(cont, nombres)
    option = int(input("¿Cual eliges?: "))
    if 1 <= option <= len(names_pkmn):
        chose_pkmn = player_profile["pokemon_inventory"][option - 1]
        return chose_pkmn
    else:
        print("Opción no válida, elige un número válido.")
        return get_choose_player_pokemon_fight(player_profile)


def get_choose_enemy_pokemon_fight(enemy_profile):

    random_pkmn = random.choice(enemy_profile['pokemon_inventory'])
    print(f"Tu contrincante ha elegido ha: {random_pkmn['name']}")
    return random_pkmn

def survival_mode(pokemon_list, player_profile):

    print("------Bienvenido al Pokemon Survival Mode------")
    print("Preparate para tu primer combate")
    clear_screen()

    while any_player_pokemon_lives(player_profile):
        enemy_profile = get_enemy_profile()
        if player_profile['combats'] < 8:
            random_num_pkmn = random.randint(1 , 3)
            enemy_pokemon = random.sample(pokemon_list,random_num_pkmn)
            enemy_profile['pokemon_inventory'].append(enemy_pokemon)
        elif 8 <= player_profile['combats'] < 15:
            random_num_pkmn = random.randint(3 , 4)
            random_num_potion = random.randint(1, 2)
            enemy_pokemon = random.sample(pokemon_list,random_num_pkmn)
            enemy_profile['pokemon_inventory'].append(enemy_pokemon)
            enemy_profile['health_potion'] = random_num_potion
        elif player_profile['combats'] < 15:
            enemy_pokemon = random.sample(pokemon_list,6)
            random_num_potion = random.randint(2, 3)
            enemy_profile['pokemon_inventory'].append(enemy_pokemon)
            enemy_profile['health_potion'] = random_num_potion

        player_pkmn_fight = get_choose_player_pokemon_fight(player_profile)
        enemy_pokemon_fight = get_choose_enemy_pokemon_fight(enemy_profile)

        if enemy_pokemon_fight['speed'] > player_pkmn_fight ['speed']:
            pass



def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile()
    choose_pokemon(pokemon_list, player_profile)
    inventory_menu(player_profile)
    choose_pokemon(pokemon_list, player_profile)
    inventory_menu(player_profile)
    get_choose_player_pokemon_fight(player_profile)

if __name__ ==  "__main__":
    main()