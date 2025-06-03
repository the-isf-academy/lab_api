from flask import Flask, request
from helpers import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    json = {'message': 'Hello from the ISF Riddles API!'}
    return json, 200

@app.route('/all', methods=['GET'])
def all_riddles():
    all_riddles = get_all_riddles()

    all_riddles_list = []
    for riddle in all_riddles:
        all_riddles_list.append(json_riddle_answerless(riddle))

    json = {'riddles': all_riddles_list}

    return json, 200

@app.route('/new', methods=['POST'])
def new_riddle():
    # get API parameters 
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    riddle = new_riddle(question, answer)

    json = {
        'message': 'Riddle added successfully.',
        'question': json_riddle(riddle)}
    
    return json, 201


if __name__ == '__main__':
    app.run(debug=True)

