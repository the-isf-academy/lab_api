from flask import Flask, request
from helpers import *

app = Flask(__name__)

BASE_URL = 'riddles'

@app.route(f'/{BASE_URL}', methods=['GET'])
def index():
    data = {'message': 'Hello from the ISF Riddles API!'}
    return data, 200

@app.route(f'/{BASE_URL}/all', methods=['GET'])
def all_riddles():
    all_riddles = get_all_riddles()

    all_riddles_json = []
    for riddle in all_riddles:
        all_riddles_json.append(json_riddle_answerless(riddle))

    return all_riddles_json, 200

@app.route(f'/{BASE_URL}/one', methods=['GET'])
def one_riddle():
    # get API parameters 
    data = request.get_json()
    id = data.get('id')
    riddle = get_one_riddle(id)

    # error handeling
    if riddle is None:
        return {'error': 'Post not found'}, 404
    
    return json_riddle_answerless(riddle), 200

@app.route(f'/{BASE_URL}/new', methods=['POST'])
def new_riddle():
    # get API parameters 
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    # error handeling
    if not question or not answer:
        return {'error': 'Question and Answer are required.'}, 404

    riddle = new_riddle(question, answer)
    
    return {
        'message': 'Riddle added successfully.',
        'question': json_riddle(riddle)}, 201

@app.route(f'/{BASE_URL}/guess', methods=['PUT'])
def guess_riddle():
    # get API parameters 

    data = request.get_json()
    id = data.get('id')
    guess = data.get('guess')

    # error handeling
    if not id or not guess:
        return {'error': 'id and guess are required.'}, 404

    riddle = get_one_riddle(id)

    # error handeling
    if riddle is None:
        return {'error': 'Post not found'}, 404

    if guess == riddle['answer']:
        riddle = update_riddle_stats(id,True)

        return {'correct': True, 'riddle': json_riddle(riddle)}, 200
    
    else:
        riddle = update_riddle_stats(id,False)
        return {'correct': False, 'riddle': json_riddle_answerless(riddle)}, 200
    

if __name__ == '__main__':
    app.run(debug=True)

