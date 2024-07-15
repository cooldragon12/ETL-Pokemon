from bs4 import BeautifulSoup
from urllib import request
from tqdm import tqdm
import logging
import time

from logger import TqdmLoggingHandler
from load import Pokemon

logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self):
        # Setting up the logger
        logger.setLevel(logging.INFO)
        logger.addHandler(TqdmLoggingHandler())
        logger.addHandler(logging.FileHandler('log/etl_pokemon.log'))
        
        # Setting up the base url
        self.base_url = "https://pokemondb.net" # Base url of the pokemondb
        self.url = self.base_url + "/pokedex/national" # main url of the pokemondb contains the list overview of the pokemons
        
        # Initiating a Opener 
        self.request = request
        self.url_opener = request.build_opener()
        self.url_opener.addheaders = [('User-Agent', 'PostmanRuntime/7.40.0')]
        self.request.install_opener(self.url_opener)
        
        # Intansiating the variables to tempory store the data
        self.loaded_data = None
        self.pokemon_collection: List[Pokemon] = []

    def preload(self):
        """Loading the html from the url of the pokemondb"""
        logger.info('Loading html from %s', self.url)
        try:
            response = self.request.urlretrieve(self.url)
            self.loaded_data = response[0] # load the data in the memory
        except Exception as e:
            logger.error('Error loading html from %s: %s', self.url, e)
            return None
        logger.info('Successfully loaded')

    def extract(self):
        """Extracting the data from the loaded data"""
        logger.info('Start Extracting data from the loaded data')
        
        with open(self.loaded_data, 'r') as f:
            bs = BeautifulSoup(f, 'html.parser')
            for gen, pokemons in enumerate(tqdm(bs.find_all("div",class_="infocard-list"))):
                # Extracting the data from each of the genration
                # collection = []
                for _,pokemon_card in enumerate(tqdm(pokemons.find_all("div", class_="infocard"))):
                    # Extracting the data from each of the pokemon card
                    pokemon_info = {}
                    pok_link = pokemon_card.find("span",class_="infocard-lg-data text-muted").find("a",class_="ent-name").get("href")
                    pokemon_info["name"] = pokemon_card.find("span",class_="infocard-lg-data text-muted").find("a",class_="ent-name").getText()
                    pokemon_info["national_no"] = pokemon_card.find("span",class_="infocard-lg-data text-muted").find("small").getText()
                    pokemon_info["generation"] = gen+1
                    types = pokemon_card.find("span",class_="infocard-lg-data text-muted").find_all("small")[1].find_all("a", class_="itype")
                    
                    # This will extract the types of the pokemon and store it in the dictionary in each column
                    if len(types) == 1:
                        pokemon_info["type0"] = types[0].getText()
                        pokemon_info["type1"] = None
                    else:
                        pokemon_info["type0"] = types[0].getText()
                        pokemon_info["type1"] = types[1].getText()

                    self.get_pokemon_info(pokemon_info, pok_link)
                    
                    pokemon_encoded = Pokemon(**pokemon_info)

                    self.pokemon_collection.append(pokemon_encoded)
                # yield collection
                #     break
                # break #For debugging purposes
        logger.info('Extraction completed')
    
    def get_pokemon_info(self, pokemon, url):
        """Extracting the data from the pokemon page"""
        logger.info('\aExtracting data info for %s from %s \a', pokemon["name"], url)
        response = self.request.urlretrieve(self.base_url+url)[0]
        with open(response, 'r', encoding="utf8") as f:
            soup = BeautifulSoup(f, 'html.parser')
            # Extracting the data
            pokemon["species"] = soup.find("th", string="Species").find_next("td").getText()
            pokemon["height"] = soup.find("th", string="Height").find_next("td").getText()
            pokemon["weight"] = soup.find("th", string="Weight").find_next("td").getText()
            # Base Stats
            pokemon["hp"] = soup.find("th", string="HP").find_next("td").getText()
            pokemon["attack"] = soup.find("th", string="Attack").find_next("td").getText()
            pokemon["defense"] = soup.find("th", string="Defense").find_next("td").getText()
            pokemon["sp_attack"] = soup.find("th", string="Sp. Atk").find_next("td").getText()
            pokemon["sp_defense"] = soup.find("th", string="Sp. Def").find_next("td").getText()
            pokemon["speed"] = soup.find("th", string="Speed").find_next("td").getText()
            pokemon["total"] = soup.find("th", string="Total").find_next("td").getText()
            
            # You can add more data to extract here if you want
            # But don't forget to add the column in the Pokemon class in load.py, and the data in the pokemon_info dictionary in the extract method
        return pokemon