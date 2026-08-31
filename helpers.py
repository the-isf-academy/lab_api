import sqlite3

def get_all_riddles():
    db_connection = sqlite3.connect("database.db")
    db_cursor = db_connection.cursor()

    all_riddles = db_cursor.execute("SELECT * FROM riddles").fetchall()

    db_connection.close()

    return all_riddles

def get_one_riddle(riddle_id):
    db_connection = sqlite3.connect("database.db")
    db_cursor = db_connection.cursor()

    one_riddle = db_cursor.execute("SELECT * FROM riddles where id = ?", (riddle_id,)).fetchone()

    db_connection.close()

    return one_riddle

def get_riddles_by_difficulty(difficulty):
    db_connection = sqlite3.connect("database.db")
    db_cursor = db_connection.cursor()

    riddles = db_cursor.execute("SELECT * FROM riddles where difficulty = ?", (difficulty,)).fetchall()

    db_connection.close()

    return riddles

def new_riddle(question, answer):
    db_connection = sqlite3.connect("database.db")
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("INSERT INTO riddles (question, answer) VALUES (?, ?)",(question, answer))


    newest_riddle = db_cursor.execute("SELECT * FROM riddles order by id desc limit 1").fetchone()


    db_connection.commit()

    return newest_riddle



def update_riddle_guessed(riddle_id, is_correct):
    db_connection = sqlite3.connect("database.db")
    db_cursor = db_connection.cursor()

    db_cursor.execute(f"UPDATE riddles set total_guesses = total_guesses + 1  where id = ? ", (riddle_id ,))

    if is_correct == True:
        db_cursor.execute(f"UPDATE riddles set correct_guesses = correct_guesses + 1  where id = ? ", (riddle_id ,))


    db_connection.commit()
    db_connection.close()



def json_riddle(riddle):
    return {
        'id': riddle[0],
        'question': riddle[1],
        'answer': riddle[2],
        'total_guesses': riddle[3],
        'correct_guesses': riddle[4],
        'difficulty': riddle[5]
    }

def json_riddle_answerless(riddle):
    return {
        'id': riddle[0],
        'question': riddle[1],
        'total_guesses': riddle[3],
        'correct_guesses': riddle[4],
        'difficulty': riddle[5]
    }

if __name__=="__main__":
    print("-- testing helper functions")

    # new_riddle('test','aa')

    riddle = get_one_riddle(2)
    print(json_riddle(riddle))

    # print(json_riddle(riddle))

    # for riddle in get_riddles_by_difficulty('easy'):
    #     print(riddle[0],riddle[1])
