import re
from requests_html import HTMLSession

pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 1,
    "level": 1,
    "type": [],
    "current_exp": 0
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="

def get_pokemon(index):
    url = f"{URL_BASE}{index}"
    session =HTMLSession()
    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    # Get Pokémon name
    new_pokemon["name"] = pokemon_page.html.find(".mini", first =True).text.split('\n')[0]

    # Get Pokémon type
    type_list= [
    "normal", "fuego", "agua", "planta", "eléctrico", "hielo",
    "lucha", "veneno", "tierra", "volador", "psíquico", "bicho",
    "roca", "fantasma", "dragón"
    ]
    type_pattern = r"/([\w-]+)\.png$"
    new_pokemon_type = pokemon_page.html.find("img")
    for img in new_pokemon_type:
        src = img.attrs.get('src', '')
        match = re.search(type_pattern, src)
        if match:
            type_found= match.group(1)
            if type_found in type_list:
                if type_found not in new_pokemon["type"]:
                    new_pokemon["type"].append(type_found)

    return new_pokemon


def main():
    print(get_pokemon(1))

if __name__ == "__main__":
    main()


