import json
from extract import Extractor
from load import Loader, Pokemon, Pokedex
from argparse import ArgumentParser

arg = ArgumentParser()
arg.add_argument("--extract", help="Extract the data from the pokemondb", action="store_true")
arg.add_argument("--start-pipeline", help="Start the pipeline", action="store_true")
arg.add_argument("--check-pokedex", help="Check the pokedex", action="store_true")

def main():
    args = arg.parse_args()
    if args.extract:
        extractor = Extractor()
        extractor.preload()
        extractor.extract()
        with open("data.json", "w") as f:
            json.dump([pokemon.__dict__ for pokemon in extractor.pokemon_collection], f)
        
    if args.start_pipeline:
        extractor = Extractor()
        extractor.preload()
        extractor.extract()
        loader = Loader(extractor.pokemon_collection)
        loader.catch_em_all()
    
    if args.check_pokedex:
        while True:
            try:
                pokedex = Pokedex()
                inp = input("""Choose which you want to do:
                
1. Get a pokemon by its national number
2. Get a pokemon by its name
3. Get a list of pokemons by their type
4. Get a list of pokemons by their generation
5. Exit
Choose: """)
                if inp == "exit" or inp == "5":
                    break
                elif inp == "1":
                    nat = input("Enter the national number of the pokemon: ")
                    nat = nat.split(",")
                    for i in nat:
                        pokedex.get_pokemon(i)
                elif inp == "2":
                    name = input("Enter the name of the pokemon: ")
                    pokedex.get_pokemon_by_name(name)
                elif inp == "3":
                    type_ = input("Enter the type of the pokemon: ")
                    pokedex.get_pokemon_by_type(type_)
                elif inp == "4":
                    gen = input("Enter the generation of the pokemon: ")
                    pokedex.get_pokemon_by_generation(gen)
                else:
                    print("Invalid input")
            except Exception as e:
                print(e)
                break
    



if __name__ == "__main__":
    main()