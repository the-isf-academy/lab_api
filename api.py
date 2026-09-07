from flask import Flask, request,jsonify
from helpers import *
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


logging.getLogger('werkzeug').setLevel(logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.before_request
def log_request_info():
    # This will run before every single request
    # Since we used ProxyFix, request.remote_addr is the REAL visitor IP
    app.logger.info('--- Incoming Request ---')
    app.logger.info(f"IP: {request.remote_addr}")
    app.logger.info(f"Path: HTTP {request.method} {request.path}")
    app.logger.info(f"User Agent: {request.headers.get('User-Agent')}\n")


BASE_URL = 'riddle'

@app.route(f'/{BASE_URL}', methods=['GET'])
def api_index():
    data = {
        'description': 'Hello from the ISF Riddles API!'
        }
    return data, 200

@app.route(f'/{BASE_URL}/help', methods=['GET'])
def api_help():
    data = {
        'GET /all':{
            'description': 'Returns all riddles without the answers',
            'payload': 'n/a'
        },
        'GET /one':{
            'description': 'Returns one riddle of a specific id',
            'payload': 'id: int'
        },
        'GET /difficulty':{
            'description': 'Returns all riddle of a specific difficulty',
            'payload': 'difficulty: str'
        },
        'POST /new':{
            'description': 'Add a new riddle to the database',
            'payload': 'question: str, answer: str'
        },
        'POST /guess':{
            'description': 'Guesses a riddle and returns if guess is correct',
            'payload': 'id: int, guess: str'
        },
    }

    return data, 200

@app.route(f'/{BASE_URL}/all', methods=['GET'])
def api_get_all_riddles():
    all_riddles = get_all_riddles()

    all_riddles_list = []
    for riddle in all_riddles:
        all_riddles_list.append(json_riddle_answerless(riddle))

    return {'riddles': all_riddles_list}, 200

@app.route(f'/{BASE_URL}/one', methods=['GET'])
def api_get_one_riddle():
    if 'id' not in  request.args:
        return {'error': 'id is required.'}, 400 
    
    # get API parameters 
    id = request.args['id']

    # get riddle from db
    riddle = get_one_riddle(id)
   
    # error handeling
    if riddle is None:
        return {'error': 'Riddle not found'}, 404
    
    return {'riddle':json_riddle_answerless(riddle)}, 200

@app.route(f'/{BASE_URL}/difficulty', methods=['GET'])
def api_get_difficulty_riddle():
    if 'level' not in  request.args:
        return {'error': 'level is required.'}, 400 

    # get API parameters 
    level = request.args['level']
    riddles = get_riddles_by_difficulty(level)

    json_riddles = []

    for riddle in riddles:
        json_riddles.append(json_riddle_answerless(riddle))

    return {
        'difficuty': level,
        'riddles': json_riddles}, 200

@app.route(f'/{BASE_URL}/new', methods=['POST'])
def api_post_new_riddle():
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



@app.route(f'/{BASE_URL}/guess', methods=['POST'])
def api_post_guess_riddle():
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

    if guess == riddle[2]:
        update_riddle_guessed(id,True)
        update_riddle_difficulty(riddle[0])
        updated_riddle = get_one_riddle(riddle[0])
        return {'correct': True, 'riddle': json_riddle(updated_riddle)}, 200
    
    else:
        update_riddle_guessed(id,False)
        update_riddle_difficulty(riddle[0])
        updated_riddle = get_one_riddle(riddle[0])
        return {'correct': False, 'riddle': json_riddle_answerless(updated_riddle)}, 200

if __name__ == '__main__':
    app.run(debug=True,port=8000)
