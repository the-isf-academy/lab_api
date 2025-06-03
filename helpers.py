import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #converts row to dictionary object
    return conn

def get_all_riddles():
    conn = get_db_connection()

    # get all Questions from database
    all_riddles = conn.execute(
        """
        SELECT *
        FROM riddles
        """).fetchall()  
    
    conn.close()

    return all_riddles

def get_one_riddle(id):
    conn = get_db_connection()

    # get all Questions from database
    riddle = conn.execute(
        """
        SELECT *
        FROM riddles
        WHERE id=?
        """,(id,)).fetchone()  
    
    conn.close()

    return riddle

def new_riddle(question, answer):
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


    riddle = get_one_riddle(id)

    difficulty_score = riddle['correct_guesses']/riddle['total_guesses']
    if difficulty_score < 0.3:
        difficult_level = "hard"
    elif difficulty_score < 0.6:
        difficult_level = "medium"
    elif difficulty_score < 1.0:
        difficult_level = "easy"

    conn.execute(
        """
        UPDATE riddles
        SET 
            difficulty = ?
        WHERE id = ?
        """,
        (difficult_level, id)
    )

    conn.commit()
    conn.close()

    return get_one_riddle(id)

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
        'difficulty': riddle['difficulty']
    }

