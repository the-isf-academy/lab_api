from flask import Flask, request,jsonify
from helpers import *

app = Flask(__name__)

BASE_URL = 'riddle'

@app.route(f'/{BASE_URL}', methods=['GET'])
def index():
    data = {'message': 'Hello from the ISF Riddles API!'}
    return data, 200

@app.route(f'/{BASE_URL}/all', methods=['GET'])
def api_all_riddles():
    all_riddles = get_all_riddles()

    all_riddles_list = []
    for riddle in all_riddles:
        all_riddles_list.append(json_riddle_answerless(riddle))

    return {'riddles': all_riddles_list}, 200

@app.route(f'/{BASE_URL}/one', methods=['GET'])
def api_one_riddle():
    if 'id' not in  request.args:
        return {'error': 'id is required.'}, 400 
    
    # get API parameters 
    id = request.args['id']

    # get riddle from db
    riddle = get_one_riddle(id)
   
    # error handeling
    if riddle is None:
        return jsonify({'error': 'Riddle not found'}), 404
    
    return jsonify({'riddle':json_riddle_answerless(riddle)}), 200

@app.route(f'/{BASE_URL}/difficulty', methods=['GET'])
def api_difficulty_riddle():
    if 'id' not in  request.args:
        return {'error': 'id is required.'}, 400 

    # get API parameters 
    id = request.args['id']
    riddle = get_one_riddle(id)

    # error handeling
    if riddle is None:
        return {'error': 'Riddle not found'}, 404
    
    return jsonify({'riddle':json_riddle_difficulty(riddle)}), 200

@app.route(f'/{BASE_URL}/random', methods=['GET'])
def api_random_riddle():
    # get API parameters    
    riddle = get_random_riddle()

    # error handeling
    if riddle is None:
        return {'error': 'Riddle not found'}, 404
    
    return json_riddle_answerless(riddle), 200

@app.route(f'/{BASE_URL}/new', methods=['POST'])
def api_new_riddle():
    # error handeling
    if 'question' not in  request.args or 'answer' not in request.args:
        return {'error': 'question and answer are required.'}, 400 
    
    # get API parameters 
    question = request.args['question']
    answer = request.args['answer']


    riddle = new_riddle(question, answer)
    
    return {
        'message': 'Riddle added successfully.',
        'question': json_riddle(riddle)}, 201

@app.route(f'/{BASE_URL}/guess', methods=['PUT'])
def api_guess_riddle():
    # get API parameters 

    # error handeling
    if 'id' not in  request.args or 'guess' not in request.args:
        return {'error': 'id and guess are required.'}, 400 
    
    # get id and guess
    id = request.args['id']
    guess = request.args['guess']

    riddle = get_one_riddle(id)

    if riddle is None:
        return {'error': 'Riddle not found'}, 404

    # error handeling
    if riddle is None:
        return {'error': 'Riddle not found'}, 404

    if guess == riddle['answer']:
        riddle = update_riddle_stats(id,True)
        return {'correct': True, 'riddle': json_riddle(riddle)}, 200
    
    else:
        print(id)
        riddle = update_riddle_stats(id,False)
        return {'correct': False, 'riddle': json_riddle_answerless(riddle)}, 200



if __name__ == '__main__':
    app.run(debug=True)

