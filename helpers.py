import sqlite3

# DATABASE INTERACTIONS

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #converts row to dictionary object
    return conn

def get_all_riddles():
    '''Returns all riddles from the database'''

    conn = get_db_connection()

    all_riddles = conn.execute(
        """
        SELECT *
        FROM riddles
        """).fetchall()  
    
    conn.close()

    return all_riddles

def get_one_riddle(id):
    '''Returns one riddles from the database
    of a specific id'''

    conn = get_db_connection()

    riddle = conn.execute(
        """
        SELECT *
        FROM riddles
        WHERE id=?
        """,(id,)).fetchone()  
    
    conn.close()

    return riddle

def get_random_riddle():
    '''Returns one random riddle from the database'''

    conn = get_db_connection()

    random_riddle = conn.execute(
        f"""
        SELECT *
        from riddles
        ORDER BY random()
        limit 1""").fetchone()   
    
    conn.close()

    return random_riddle

def new_riddle(question, answer):
    '''Inserts a new riddle into the database
    Returns the new riddle'''


    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO 
        riddles (question, answer) 
        VALUES (?, ?)""",
        (question, answer)
    )

    conn.commit()

    new_riddle = conn.execute(
        """
        SELECT * 
        FROM riddles 
        ORDER BY id desc
        LIMIT 1
        """).fetchone()

    conn.close()

    return new_riddle

def update_riddle_stats(id, correct):
    '''Updates total_guesses and corect_guesses column
    for one riddle of a given id'''


    conn = get_db_connection()

    conn.execute(
        """
        UPDATE riddles
        SET 
            total_guesses = total_guesses + 1,
            correct_guesses = correct_guesses + CASE WHEN ? THEN 1 ELSE 0 END
        WHERE id = ?
        """,
        (correct, id)
    )
    conn.commit()

    conn.execute(
        """
        UPDATE riddles
        SET 
            difficulty = CAST(correct_guesses as FLOAT)/total_guesses
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return get_one_riddle(id)


# FORMATS RIDDLE JSON

def json_riddle(riddle):
    return {
        'id': riddle['id'],
        'question': riddle['question'],
        'answer': riddle['answer'],
        'total_guesses': riddle['total_guesses'],
        'correct_guesses': riddle['correct_guesses'],
        'difficulty': riddle['difficulty']
    }

def json_riddle_answerless(riddle):
    return {
        'id': riddle['id'],
        'question': riddle['question'],
        'total_guesses': riddle['total_guesses'],
        'correct_guesses': riddle['correct_guesses'],
    }

def json_riddle_difficulty(riddle):
    return {
        'id': riddle['id'],
        'question': riddle['question'],
        'total_guesses': riddle['total_guesses'],
        'correct_guesses': riddle['correct_guesses'],
        'difficulty': riddle['difficulty']
    }


if __name__=="__main__":
    print("[testing helper functions]")

    print(" -- testing all riddles")
    all_riddles = get_all_riddles()
    for riddle in all_riddles[0:3]:
        print(riddle['id'], riddle['question'])

    print()
    print(" -- testing one riddle")

    riddle = get_one_riddle(2)
    print(riddle['question'])
    print(json_riddle(riddle))
