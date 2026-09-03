import sqlite3
import json
import random

# connect to database
connection = sqlite3.connect('database.db')

# open riddles.sql 
with open('riddles.sql') as file:
    connection.executescript(file.read())

# create connection to database
conn = connection.cursor()

# Open and read the JSON file
with open('riddles.json', 'r') as file:
    riddles = json.load(file)
    
# create new riddles in the database
for riddle in riddles[0:11]:
    # total_guesses = random.randint(10,50)
    # correct_guesses = random.randint(0,total_guesses)
    # percentage_correct = correct_guesses/total_guesses
    # if percentage_correct < 0.3:
    #     difficulty = 'hard'
    # elif 0.3 < percentage_correct < 0.6:
    #     difficulty = 'medium'
    # else:
    #     difficulty = 'easy'


    conn.execute(
        """
        INSERT INTO riddles (question, answer, total_guesses, correct_guesses, difficulty)
        VALUES (?, ?, ?, ?, ?)
        """,
        (riddle['question'], riddle['answer'], 0, 0, 'easy')
    )

# save new riddles to database
connection.commit()

# close database
connection.close()

print("-- database initalized --")