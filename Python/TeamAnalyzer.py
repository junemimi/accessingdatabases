import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

conn = sqlite3.connect("../pokemon.sqlite")

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    c = conn.cursor()

    # finding pokedex_number and printing first line
    pokedex_number = arg
    print("Analyzing " + pokedex_number)

    # finding the name value, storing it, and removing unnecessary characters
    name_query = ("SELECT name FROM pokemon WHERE pokedex_number = " + pokedex_number)
    c.execute(name_query)
    namerun = c.fetchone()
    name = namerun[0]
    
    # finding the type1 of given pokemon, storing it, and removing unnecessary characters
    type1_query = ("SELECT name FROM type JOIN pokemon_type ON type.id = pokemon_type.type_id WHERE pokemon_type.pokemon_id = " + pokedex_number + " AND pokemon_type.which = 1")
    c.execute(type1_query)
    type1run = c.fetchone()
    type1 = type1run[0]

    # finding the type2 of given pokemon (if it exists), storing it, and removing unnecessary characters
    type2_query = ("SELECT name FROM type JOIN pokemon_type ON type.id = pokemon_type.type_id WHERE pokemon_type.pokemon_id = " + pokedex_number + " AND pokemon_type.which = 2")
    c.execute(type2_query)
    type2run = c.fetchone()
    type2 = type2run[0]

    # finding which types the given pokemon is strong and weak against, and adding them to respective lists
    against_query = "SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name = '" + type1 + "' AND type2name = '" + type2 + "'"

    for valueA, typeA in enumerate(types):
        strong_against = []
        weak_against = [] 
        c.execute(against_query) 
        against_values = c.fetchone()

    for valueB, typeB in enumerate(against_values): 
        if typeB > 1:
            strong_against.append(types[valueB])
        elif typeB < 1:
            weak_against.append(types[valueB])

    # printing second line
    print(name + " (" + type1 + " " + type2 + ") is strong against ", strong_against, " but weak against ", weak_against)

conn.close()        

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")