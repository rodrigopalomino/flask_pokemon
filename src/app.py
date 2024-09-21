from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/pokemon")
def getPokemon():
    listPokemons = []

    requestNroPokemon = requests.get("https://pokeapi.co/api/v2/pokemon")
    nroPokemons = requestNroPokemon.json()
    nroPokemons = nroPokemons["count"]

    for x in range(1, 1000):
        requestPokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{x}")
        pokemon = requestPokemon.json()

        requestPokemonDescripcion = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{x}")
        pokemonDescripcion = requestPokemonDescripcion.json()

        descripcion = ""
        for y in pokemonDescripcion["flavor_text_entries"]:
            if y["language"]["name"] == "es" and y["version"]["name"] == "alpha-sapphire":
                descripcion = y["flavor_text"]
                break

        habilidades = []
        for habilidad in pokemon["abilities"]:
            requestHabilidad = requests.get(habilidad["ability"]["url"])
            responseHabilidad = requestHabilidad.json()
            for idioma in responseHabilidad["names"]:
                if idioma["language"]["name"] == "es":
                    habilidades.append(idioma["name"])
                    break

        tipos = []
        debilidades = []
        for tipo in pokemon["types"]:
            requestTipo = requests.get(tipo["type"]["url"])
            responseTipo = requestTipo.json()
            tipo_nombre = None
            tipo_id = None
            for idioma in responseTipo["names"]:
                if idioma["language"]["name"] == "es":
                    tipo_nombre = idioma["name"]
                    tipo_id = responseTipo["id"]
                    break
            if tipo_nombre and tipo_id:
                tipos.append({"tipo": tipo_nombre, "id": tipo_id})

            damage_relations = responseTipo["damage_relations"]
            for weakness in damage_relations["double_damage_from"]:
                requestDebilidad = requests.get(weakness["url"])
                responseDebilidad = requestDebilidad.json()
                debilidad_nombre = None
                debilidad_id = None
                for idioma in responseDebilidad["names"]:
                    if idioma["language"]["name"] == "es":
                        debilidad_nombre = idioma["name"]
                        debilidad_id = responseDebilidad["id"]
                        break
                if debilidad_nombre and debilidad_id:
                    debilidades.append(
                        {"tipo": debilidad_nombre, "id": debilidad_id})

        evolutions_url = pokemonDescripcion["evolution_chain"]["url"]
        requestEvolutions = requests.get(evolutions_url)
        evolution_chain = requestEvolutions.json()

        def get_evolution_details(chain):
            evolutions = []
            while chain:
                species_name = chain["species"]["name"]
                species_id = requests.get(chain["species"]["url"]).json()["id"]
                evolution_details = {
                    "nombre": species_name,
                    "nivel_evolucion": 0,
                    "id": species_id
                }
                for detail in chain.get("evolution_details", []):
                    if "min_level" in detail:
                        evolution_details["nivel_evolucion"] = detail["min_level"]

                evolutions.append(evolution_details)
                chain = chain.get("evolves_to", [])[
                    0] if chain.get("evolves_to") else None

            return evolutions

        evolutions = get_evolution_details(
            evolution_chain["chain"])

        pokemonJson = {
            "id": pokemon["id"],
            "nombre": pokemon["forms"][0]["name"],
            "description": descripcion,
            "urlImg": pokemon["sprites"]["front_default"],
            "urlGif": pokemon["sprites"]["other"]["showdown"]["front_default"],
            "peso": pokemon["weight"],
            "tamaño": pokemon["height"],
            "stats": {
                "ps": pokemon["stats"][0]["base_stat"],
                "ataque": pokemon["stats"][1]["base_stat"],
                "defensa": pokemon["stats"][2]["base_stat"],
                "ataqueEspecial": pokemon["stats"][3]["base_stat"],
                "defensaEspecial": pokemon["stats"][4]["base_stat"],
                "velocidad": pokemon["stats"][5]["base_stat"],
                "total": (
                    pokemon["stats"][0]["base_stat"] +
                    pokemon["stats"][1]["base_stat"] +
                    pokemon["stats"][2]["base_stat"] +
                    pokemon["stats"][3]["base_stat"] +
                    pokemon["stats"][4]["base_stat"] +
                    pokemon["stats"][5]["base_stat"]
                )
            },
            "otros_stats": {
                "felicidad": pokemonDescripcion["base_happiness"],
                "ratioCaptura": pokemonDescripcion["capture_rate"]
            },
            "habilidades": habilidades,
            "tipos": tipos,
            "debilidades": debilidades,
            "evoluciones": evolutions
        }
        listPokemons.append(pokemonJson)

    return jsonify(listPokemons)


if __name__ == "__main__":
    app.run(debug=True)
