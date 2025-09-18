from flask import Flask, request
from helpers import *

app = Flask(__name__)

BASE_URL = "riddle"

@app.route(f'/{BASE_URL}', methods=['GET'])
def index():
    return {'message': 'Hello from the ISF Riddles API!'}, 200

@app.route(f'/{BASE_URL}/all', methods=['GET'])
def api_all_riddles():
    all_riddles = get_all_riddles()

    all_riddles_list = []
    for riddle in all_riddles:
        all_riddles_list.append(json_riddle_answerless(riddle))

    return {'riddles': all_riddles_list}, 200


@app.route(f'/{BASE_URL}/new', methods=['POST'])
def api_new_riddle():
    # error handeling
    if 'question' not in  request.args or 'answer' not in request.args:
        return {'error': 'question and answer are required.'}, 400 
    
    # get payload 
    question = request.args['question']
    answer = request.args['answer']

    # get riddle from db
    riddle = new_riddle(question, answer)

    return {
        'message': 'Riddle added successfully.',
        'question': json_riddle(riddle)}, 201

@app.route(f'/{BASE_URL}/one', methods=['GET'])
def api_one_riddle():
    # error handeling
    if 'id' not in  request.args:
        return {'error': 'id is required.'}, 400 
    
    id = request.args['id']

    # get riddle from db
    riddle = json_riddle_answerless(get_one_riddle(id))

    if riddle is None:
      return {'error': 'Riddle not found'}, 404

    return {'riddle': riddle}, 200

@app.route(f'/{BASE_URL}/random', methods=['GET'])
def api_random_riddle():
    
    # get a random riddle from db
    random_riddle = get_random_riddle()
    riddle = json_riddle_answerless(random_riddle)    

    return {'riddle': riddle}, 200

@app.route(f'/{BASE_URL}/guess', methods=['PUT'])
def api_guess_riddle():
    # error handeling
    if 'id' not in  request.args or 'guess' not in request.args:
        return {'error': 'id and guess are required.'}, 400 
    
    # get payload 
    id = request.args['id']
    guess = request.args['guess']

    # get the riddle with id
    riddle = json_riddle(get_one_riddle(id))

    # check if the riddle exists
    if riddle is None:
      return {'error': 'Riddle not found'}, 404
    
    else:
        # check against the answer
        if guess == riddle['answer']:
            return {'correct': 'true',
            'riddle': json_riddle(riddle)}, 200
        else:
            return{'correct': 'false',
            'riddle': json_riddle_answerless(riddle)}, 200
        
@app.route(f'/{BASE_URL}/all/<string:difficulty>', methods=['GET'])
def all_riddles_difficulty(difficulty):
    difficulty_riddles = get_difficulty_riddle(difficulty)

    all_difficulty_riddles_list = []
    for riddle in difficulty_riddles:
        all_difficulty_riddles_list.append(json_riddle_answerless(riddle))
    
    return {
        "difficulty_level": difficulty,
        "riddles": all_difficulty_riddles_list
    }, 200

if __name__ == '__main__':
    app.run(debug=True)

