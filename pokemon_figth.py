import random
import os
import time
from pokeload import get_all_pokemon, get_pokemon

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_player_profile():
    return {
        "player name": input("¿Cual es tu nombre?: "),
        "pokemon_inventory": ["Hos"],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }

def inventory(player_profile):
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
                for cont, nombres in enumerate(player_profile['pokemon_inventory'], start=1):
                    clear_screen()
                    input(f'''+--------------------------------------------------+
|                    Inventario                    |
+--------------------------------------------------+
Pokemon: {player_profile['pokemon_inventory']}        
+--------------------------------------------------+
Presione ENTER para volver al menu de inventario... ''')

            elif option == 4:
                clear_screen()
                print("Saliendo del inventario...")
                time.sleep(2)
                break

            else:
                print("Opción no válida. Por favor, elija entre 1, 2, 3 o 4.")

        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")
            time.sleep(2)
    return


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def choose_pokemon(pokemon_list, player_profile):
    chosen = None
    random_pokemon = random.sample(pokemon_list, 3)
    random_names = [pkm["name"] for pkm in random_pokemon]
    while not chosen:
        print("Elige uno de estos 3 Pokemon que te ha dejado el Profesor Elias")
        for cont, nombres in enumerate(random_names, start = 1):
            print(cont, nombres)
        try:
            option = int(input("¿Cual eliges?: "))
            if option == 1:
                return player_profile['pokemon_inventory'].append(random_names[0])
            elif option == 2:
                return player_profile['pokemon_inventory'].append(random_names[1])
            elif option == 3:
                return player_profile['pokemon_inventory'].append(random_names[2])

        except (ValueError, IndexError):
            print("Opción invalida")
    return


def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile()
    choose_pokemon(pokemon_list, player_profile)
    inventory(player_profile)

if __name__ ==  "__main__":
    main()