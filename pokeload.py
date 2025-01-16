import pickle
from requests_html import HTMLSession


pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 1,
    "level": 1,
    "type": [],
    "current_exp": 0,
    "attacks": []
}
URL_BASE_POKEMON = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="
URL_MOVESET = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

def get_pokemon(index):
    if index in {30, 50, 83}:
        return {}

    session =HTMLSession()
    url = f"{URL_BASE_POKEMON}{index}"
    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    # Get Pokémon name
    new_pokemon["name"] = pokemon_page.html.find(".mini", first =True).text.split('\n')[0]

    # Get Pokémon type

    td_type = pokemon_page.html.find("td")[16]
    img_type = td_type.find("img")
    new_pokemon["type"] = [img.attrs.get("alt") for img in img_type if "alt" in img.attrs]

    # Get Pokémon move set
    url_move_set= f"{URL_MOVESET}{index}"
    pokemon_move_set_page = session.get(url_move_set)

    for attack_item in (pokemon_move_set_page.html.find(".pkmain")[-1].find(".sortable.left", first=True).find
                       (".check3.bazul")):
        attack ={
            "name": attack_item.find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "min level": attack_item.find("th", first=True).text,
            "damege": int(attack_item.find("td")[3].text.replace("--","0")),
        }  
        new_pokemon["attacks"].append(attack)

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

