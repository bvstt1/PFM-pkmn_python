import random
import os
import time
from time import sleep
from pokeload import get_all_pokemon

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

# Funcion usada para iniciar combates
def any_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


# Se define los ataques que tendra el pokemon dependiendo del nivel
def attacks_pokemon(pokemon):
    return[attack for attack in pokemon["attacks"] if attack["min level"] <= pokemon["level"]]


#Elegir el pokemon inicial (las siguientes dos funciones), aparece despues de la presentacion del profesor
def choose_initial_pkmn_player_stats(random_pokemon, player_profile, option):
    chosen_pokemon = random_pokemon[option - 1]
    chosen_pokemon["level"] = 5
    chosen_pokemon['attacks'] = attacks_pokemon(chosen_pokemon)
    player_profile['pokemon_inventory'].append(chosen_pokemon)
    return chosen_pokemon

def choose_initial_pokemon(pokemon_list, player_profile):
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
                return choose_initial_pkmn_player_stats(random_pokemon, player_profile, option)
            elif option == 2:
                return choose_initial_pkmn_player_stats(random_pokemon, player_profile, option)
            elif option == 3:
                return choose_initial_pkmn_player_stats(random_pokemon, player_profile, option)

        except (ValueError, IndexError):
            print("Opción invalida")
    return

#Funcion para elegir el pokemon al iniciar el combate o al cambiar de pokemon
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



def get_enemy_profile():
    return {
        "pokemon_inventory": [],
        "health_potion": 0,
    }


def get_choose_enemy_pokemon_fight(enemy_profile):
    chose_pkmn = random.choice(enemy_profile['pokemon_inventory'])
    chose_pkmn['level'] = random.randint(3, 5)
    chose_pkmn['attack'] = attacks_pokemon(chose_pkmn)
    print(f"Tu contrincante ha elegido ha: {chose_pkmn['name']}")
    return chose_pkmn


def pokemon_state(chosen_attack, pkmn_attacked, pkmn_received):

    CHOSEN_NAME = chosen_attack['name']

    pkmn_attacked_attack_original = pkmn_attacked['attack']
    pkmn_attacked_defense_original = pkmn_attacked['defense']
    pkmn_attacked_speed_original = pkmn_attacked['speed']

    pkmn_received_attack_original = pkmn_received['attack']
    pkmn_received_defense_original = pkmn_received['defense']
    pkmn_received_speed_original = pkmn_received['speed']

    # Defense
    if CHOSEN_NAME == ["Refugio"]:
        pkmn_attacked["defense"] += 2
        print(f"La dsefensa de {pkmn_attacked['name']} ha subido!")

    elif CHOSEN_NAME == ["Ataque Arena", 'Chirrido']:
        pkmn_received["defense"] -= 2
        print(f"El ataque de {pkmn_attacked['name']} ha subido!")

    # Attack
    elif CHOSEN_NAME == ["Afilar","Danza espada", "Desarrollo"]:
        pkmn_attacked["attack"] += 2
        print(f"El ataque de {pkmn_attacked['name']} ha subido!")

    # Speed
    elif CHOSEN_NAME == ["Disparo Demora", "Conversión", "Destello"]:
        pkmn_received['speed'] -= 2
        print(f"La velocidad de {pkmn_received['name']} ha bajado!")

    elif CHOSEN_NAME == ['Doble equipo']:
        pkmn_attacked["speed"] += 2
        print(f"El ataque de {pkmn_attacked['name']} ha subido!")

    # States
    elif CHOSEN_NAME == ['Onda Trueno', "Deslumbrar"]:
        # pkmn_recived se paraliza
        pass

    elif CHOSEN_NAME == ['Rayo Confuso']:
        # pkmn_recived se confunde
        pass

    elif CHOSEN_NAME == ['Beso Amoroso', 'Canto']:
        # Duerme al rival
        pass

    elif CHOSEN_NAME == ['Neblina', 'Niebla', 'Anulación']:

        pkmn_attacked['attack'] = pkmn_attacked_attack_original
        pkmn_attacked['defense'] = pkmn_attacked_defense_original
        pkmn_attacked['speed'] = pkmn_attacked_speed_original

        pkmn_received['attack'] = pkmn_received_attack_original
        pkmn_received['defense'] = pkmn_received_defense_original
        pkmn_received['speed'] = pkmn_received_speed_original

        print("Se han restaurados las estadisticas de ambos pokemon!")

    elif CHOSEN_NAME == ['Ventisca']:
        # probabilidad del 10% de conjelar al rival
        pass

    elif CHOSEN_NAME == ["Amortiguador "]:
        if pkmn_attacked['current_health'] == pkmn_attacked["base_health"]/2:
            print(f"{pkmn_attacked['name']} ha fallado el ataque!")
        else:
            pkmn_attacked['current_health'] += pkmn_attacked["base_health"]/2
            if pkmn_attacked['current_health'] > pkmn_attacked["base_health"]:
                pkmn_attacked['current_health'] = pkmn_attacked["base_health"]
            print(f"La vida de {pkmn_attacked['name']} se ha restaurtado a la mitad")


def survival_mode(pokemon_list, player_profile):
    print("------Bienvenido al Pokemon Survival Mode------")
    print("Preparate para tu primer combate")
    clear_screen()

    while any_pokemon_lives(player_profile):
        enemy_profile = get_enemy_profile()

        # Dependiendo del numero de combates que tenga el jugador, la probabilidad en la cantidad de Pokémon que
        # tenga el enemigo sube, con un limite de 6

        if player_profile['combats'] < 8:
            random_num_pkmn = random.randint(1 , 3)
            enemy_pokemon = random.sample(pokemon_list,random_num_pkmn)
            enemy_profile['pokemon_inventory'].extend(enemy_pokemon)

        elif 8 <= player_profile['combats'] < 15:
            random_num_pkmn = random.randint(3 , 4)
            random_num_potion = random.randint(1, 2)
            enemy_pokemon = random.sample(pokemon_list,random_num_pkmn)
            enemy_profile['pokemon_inventory'].extend(enemy_pokemon)
            enemy_profile['health_potion'] = random_num_potion

        elif player_profile['combats'] >= 15:
            enemy_pokemon = random.sample(pokemon_list,6)
            random_num_potion = random.randint(2, 3)
            enemy_profile['pokemon_inventory'].extend(enemy_pokemon)
            enemy_profile['health_potion'] = random_num_potion

        #Elección de Pokemon dependiendo de los que se tengan en el inventario

        player_pkmn_fight = get_choose_player_pokemon_fight(player_profile)
        enemy_pokemon_fight = get_choose_enemy_pokemon_fight(enemy_profile)

        #Comienza el combate
        while any_pokemon_lives(enemy_profile):
            if enemy_pokemon_fight['speed'] > player_pkmn_fight ['speed']:
                #Turno del contrincante
                print("Comienza tu contrincante")
                random_enemy_attack = random.randint(0, len(enemy_pokemon_fight['attacks'] - 1))
                chosen_attack = enemy_pokemon_fight["attacks"][random_enemy_attack]
                print(f"El {enemy_pokemon_fight['name']} de tu contrincante ha usado {chosen_attack['name']}")
                input("Preciona ENTER para continua...")
                clear_screen()

                #Turno del jugador
                print("Es tu turno")
                print(f"Que hara {player_pkmn_fight['name']}?")
                action = input("A) Atacar, B) Mochila, C) Cambiar, D)Rendirse")
                if action == "A":
                    clear_screen()
                    attacks_name = [attack["name"] for attack in player_pkmn_fight['attacks']]
                    print(f"¿Que ataque realizara {player_pkmn_fight['name']}?")
                    for cont, attack in enumerate(attacks_name, start=1):
                        print(f"{cont}. {attack}")

                    try:
                        option = int(input("¿Cual eliges?: "))
                        if 1 <= option <= len(player_pkmn_fight["attacks"]):
                            chosen_attack = player_pkmn_fight["attacks"][option - 1]
                            print(f"{player_pkmn_fight['name']} uno {chosen_attack['name']}!")
                        else:
                            print("Número inválido, elige una opción correcta.")
                    except ValueError:
                        print("Entrada inválida, ingresa un número.")

                elif action == "B":
                    clear_screen()
                    print("Tienes estos objetos")
                    print(f"1. Pociones: {player_profile['health_potion']}")
                    print(f"2. Pokebolas: {player_profile['pokeballs']}")

                    option = input("¿Qué decides hacer?: ")
                    if option == "1":
                        if player_profile["health_potion"] > 0:
                            if player_pkmn_fight["current_health"] < player_pkmn_fight["base_health"]:
                                player_pkmn_fight["current_health"] += 20
                                if player_pkmn_fight["current_health"] > player_pkmn_fight["base_health"]:
                                    player_pkmn_fight["current_health"] = player_pkmn_fight["base_health"]
                                player_profile["health_potion"] -= 1
                                print(
                                    f"{player_pkmn_fight['name']} ha recuperado 20 puntos de vida. Salud actual: "
                                    f"{player_pkmn_fight['current_health']}/{player_pkmn_fight['base_health']}")
                            else:
                                print(f"{player_pkmn_fight['name']} ya tiene la salud al máximo.")
                        else:
                            print("No tienes pociones disponibles.")

                    elif option == "2":
                        print("No puedes usar pokebolas en este modo.")

                    else:
                        print("Opción inválida, elige 1 o 2.")

                elif action == "C":
                    player_pkmn_fight = get_choose_player_pokemon_fight(player_profile)

                elif action == "D":
                    clear_screen()
                    print("Haz decidido rendirte, saldras del Survival Mode")
                    sleep(1)
                    return



def main ():
    pass

if __name__ ==  "__main__":
    main()