from dataclasses import dataclass
from sqlite3 import connect
import logging
import time
import pandas as pd
logger = logging.getLogger(__name__)

class BaseManager:
    def __init__(self):
        self.conn = connect('pokedex.db')
        self.cursor = self.conn.cursor()
        
    def __del__(self):
        self.conn.close()

# This datavlass will ensure that the data is stored in the correct format
# This will also help in the type hinting
@dataclass
class Pokemon:
    national_no:str
    name: str
    type0:str
    type1:str | None
    generation:int
    species:str
    height:str
    weight:str
    # Base Stats
    hp:int
    attack:int
    defense:int
    sp_attack:int
    sp_defense:int
    speed:int
    total:int


class Loader(BaseManager):
    def __init__(self, extracted_data=None):
        super().__init__()
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(logging.FileHandler('log/etl_pokemon.log'))

        logger.info('Checking if the table exists')
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (
                                name TEXT, 
                                national_no TEXT PRIMARY KEY, 
                                type0 TEXT, 
                                type1 TEXT NULL, 
                                generation INTEGER, 
                                height TEXT, 
                                weight TEXT, 
                                species TEXT, 
                                hp INTEGER, 
                                attack INTEGER, 
                                defense INTEGER, 
                                sp_attack INTEGER, 
                                sp_defense INTEGER, 
                                speed INTEGER, 
                                total INTEGER)""")
        self.extracted_data = extracted_data
    
    def catch_em_all(self):
        logger.info('Catching pokemons in process')
        try:
            self.cursor.executemany("INSERT INTO pokemon VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                                [
                                    (
                                        pokemon.name, 
                                        pokemon.national_no, 
                                        pokemon.type0, 
                                        pokemon.type1, 
                                        pokemon.generation,
                                        pokemon.height, 
                                        pokemon.weight, 
                                        pokemon.species,
                                        pokemon.hp,
                                        pokemon.attack,
                                        pokemon.defense,
                                        pokemon.sp_attack,
                                        pokemon.sp_defense,
                                        pokemon.speed, 
                                        pokemon.total
                                    ) for pokemon in self.extractor.pokemon_collection])
            self.conn.commit()
        except Exception as e:
            logger.error('Error loading data to the database: %s', e)
            logger.info('The data will be saved in a json file')
            import json
            with open('pokemon.json', 'w') as f:
                f.write(json.dumps(self.extractor.pokemon_collection.__dict__))
        logger.info('Successfully loaded the data into the database')
        self.count_loaded()
    
    def count_loaded(self):
        self.cursor.execute("SELECT COUNT(*) FROM pokemon")
        logger.info('Total number of pokemons loaded: %s', self.cursor.fetchone()[0])

def show_in_log(func):
    """Shows the result of the function in the log"""
    def wrapper(*args, **kwargs):
        timestamp = time.time()
        data = func(*args, **kwargs)

        pandas_data = pd.DataFrame(data, columns=Pokemon.__annotations__.keys())
        print(pandas_data, end="\n\n")
        return data
    return wrapper

class Pokedex(BaseManager):
    def __init__(self):
        super().__init__()
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(logging.FileHandler('log/etl_pokemon.log'))
    
    @show_in_log
    def get_pokemon(self, national_no):
        self.cursor.execute("SELECT * FROM pokemon WHERE national_no=?", (national_no,))
        return self.cursor.fetchone()
    
    @show_in_log
    def check_pokedex(self):
        self.cursor.execute("SELECT * FROM pokemon")
        return self.cursor.fetchall()
    
    @show_in_log
    def get_pokemon_by_name(self, name):
        self.cursor.execute("SELECT * FROM pokemon WHERE name=?", (name,))
        return self.cursor.fetchone()
    
    @show_in_log
    def get_pokemon_by_generation(self, generation):
        self.cursor.execute("SELECT * FROM pokemon WHERE generation=?", (generation,))
        return self.cursor.fetchall()
    
    @show_in_log
    def get_pokemon_by_type(self, type_):
        self.cursor.execute("SELECT * FROM pokemon WHERE type0=? OR type1=?", (type_.capitalize(), type_.capitalize()))
        return self.cursor.fetchall()

