# api.py
# ---
# to run a local server: python api.py

from flask import Flask, request
from helpers import *

app = Flask(__name__)

BASE_URL = "riddle"

@app.route(f'/{BASE_URL}', methods=['GET'])
def index():
    return {'message': 'Hello from the ISF Riddles API!'}, 200

@app.route(f'/{BASE_URL}/all', methods=['GET'])
def api_all_riddles():
    # get all riddles from database
    all_riddles = get_all_riddles()

    # store riddle in a list in proper JSON format
    all_riddles_list = []
    for riddle in all_riddles:
        all_riddles_list.append(json_riddle_answerless(riddle))

    # return success JSON
    return {'riddles': all_riddles_list}, 200


@app.route(f'/{BASE_URL}/new', methods=['POST'])
def api_new_riddle():
    # error handeling if payload is not provided
    if 'question' not in  request.args or 'answer' not in request.args:
        return {'error': 'question and answer are required.'}, 400 
    
    # get payload 
    question = request.args['question']
    answer = request.args['answer']

    # get riddle from database
    riddle = new_riddle(question, answer)

    # return success JSON
    return {
        'message': 'Riddle added successfully.',
        'question': json_riddle(riddle)}, 201




if __name__ == '__main__':
    app.run(debug=True)

