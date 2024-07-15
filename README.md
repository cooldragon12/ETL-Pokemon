# ETL Pokemon Data
This activity is to extract, transform, and load a Pokemon dataset into a SQL database. The data is from the [Pokemon Database](https://pokemondb.net/pokedex/national). The dataset contains information about 800 Pokemon from all 10 generations. The data includes columns for the Pokemon's type, stats, and more.

## Pipeline
The ETL process is broken down into three main steps:

1. Extract: Extract the data from the Pokemon Database
2. Transform: Transform the data into a usable format like dictionaries/json
3. Load: Load the data into a SQL database

### Extract & Transform
The data was srapped from the [Pokemon Database](https://pokemondb.net/pokedex/national) using the following libraries:

- urllib
- BeautifulSoup

### Load
The data was loaded into a SQL database using the following libraries:

- sqlite3

adding additional columns to the dataset to make it more useful.

---

#### Database Schema
The database schema is as follows:
Pokemon:
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


## Logger

I also included a logger to log the process of the ETL. The logger logs the following:

- The extraction process
- The transformation process
- The loading process

The logger is streamed in terminal and saved in a log file. The log file is named `etl_pokemon.log`.


## Usage
To run the ETL process, run the following command in terminal:

```bash
python main.py --start-pipeline|--extract|--check-pokedex
```

The `--start-pipeline` flag will run the entire ETL process. 
The `--extract` flag will only run the extraction process and export to json. 
The `--check-pokedex` flag will check the pokedex for any missing Pokemon.

