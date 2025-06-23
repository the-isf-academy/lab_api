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
    # get API parameters 
    data = request.get_json()
    id = data.get('id')
    riddle = get_one_riddle(id)
    print(riddle)
    # error handeling
    if riddle is None:
        return {'error': 'Post not found'}, 404
    
    return jsonify({'riddle':json_riddle_answerless(riddle)}), 200

@app.route(f'/{BASE_URL}/random', methods=['GET'])
def api_random_riddle():
    # get API parameters    
    riddle = get_random_riddle()

    # error handeling
    if riddle is None:
        return {'error': 'Post not found'}, 404
    
    return json_riddle_answerless(riddle), 200

@app.route(f'/{BASE_URL}/new', methods=['POST'])
def api_new_riddle():
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
def api_guess_riddle():
    # get API parameters 
    data = request.get_json()
    id = data.get('id')
    guess = data.get('guess')
    # error handeling
    if not id or not guess:
        return {'error': 'id and guess are required.'}, 404
    riddle = get_one_riddle(id)
    print(riddle['id'])

#    return {'r':0}


    # error handeling
    if riddle is None:
        return {'error': 'Post not found'}, 404

    if guess == riddle['answer']:
        riddle = update_riddle_stats(id,True)
        return {'correct': True, 'riddle': json_riddle(riddle)}, 200
    
#    return {'r':0}
    else:
        riddle = update_riddle_stats(id,False)
        return {'correct': False, 'riddle': json_riddle_answerless(riddle)}, 200



if __name__ == '__main__':
    app.run(debug=True)

