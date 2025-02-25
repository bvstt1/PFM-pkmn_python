import pickle
import pprint
import copy
from requests_html import HTMLSession

pokemon_base = {
    "name": "",
    "current_health": None,
    "base_health": None,
    "level": None,
    "current_exp": 0,
    "attack": None,
    "defense": None,
    "speed": None
}
URL_BASE_POKEMON = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="
URL_MOVESET = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="
URL_BASE_HEALTH = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/stats&pk="

def get_pokemon(index):
    if index in {30, 50, 83}:
        return {}

    session = HTMLSession()
    url = f"{URL_BASE_POKEMON}{index}"
    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    # Get Pokémon name
    new_pokemon["name"] = pokemon_page.html.find(".mini", first =True).text.split('\n')[0]

    # Get Pokémon type
    POKEMON_TYPES = ["normal","fuego","agua","electrico","planta","hielo","lucha","veneno","tierra","volador","psiquico",
                     "bicho","roca","fantasma","dragon"] # First generation types
    td_type = pokemon_page.html.find("td")[16]
    img_type = td_type.find("img")
    pokemon_type = set([img.attrs.get("alt") for img in img_type if "alt" in img.attrs])
    new_pokemon["type"] = []
    for pkmn_type in pokemon_type:
        if pkmn_type in POKEMON_TYPES:
            new_pokemon["type"].append(pkmn_type)

    # Get Pokémon move set
    url_move_set= f"{URL_MOVESET}{index}"
    pokemon_move_set_page = session.get(url_move_set)
    new_pokemon["attacks"] = []
    for attack_item in (pokemon_move_set_page.html.find(".pkmain")[-1].find(".sortable.left", first=True).find
                       (".check3.bazul")):
        attack ={
            "name": attack_item.find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "min level": attack_item.find("th", first=True).text,
            "damege": int(attack_item.find("td")[3].text.replace("--","0")),
        }  
        new_pokemon["attacks"].append(attack)

    # Get Pokémon base and current health
    url_base_health = f"{URL_BASE_HEALTH}{index}"
    pokemon_base_healt_page = session.get(url_base_health)
    pokemon_base_health =  pokemon_base_healt_page.html.find("td.right", first =True).text.split("\n")[0]
    new_pokemon["base_health"] = int(pokemon_base_health)
    new_pokemon["current_health"] = int(pokemon_base_health)

    # Get Pokémon attack
    pokemon_attack =  pokemon_base_healt_page.html.find("td.right")[2].text.split("\n")[0]
    new_pokemon["attack"] = int(pokemon_attack)

    # Get Pokémon defense
    pokemon_defense =  pokemon_base_healt_page.html.find("td.right")[4].text.split("\n")[0]
    new_pokemon["defense"] = int(pokemon_defense)

    # Get Pokémon speed
    pokemon_speed =  pokemon_base_healt_page.html.find("td.right")[6].text.split("\n")[0]
    new_pokemon["speed"] = int(pokemon_speed)

    return new_pokemon

def get_all_pokemon():
    try:
        print("Cargando el archivo de Pokémons")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemon=pickle.load(pokefile)

    except FileNotFoundError:
        print("¡Archivo no encontrado! Cargando de internet...")
        all_pokemon = []
        for index in range(150):
            all_pokemon.append(get_pokemon(index+1))
            print("*", end="")
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemon, pokefile)
        print("\nTodos los Pokémon han sido descargados")
    return all_pokemon