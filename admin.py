#-----------------------------------------------------------------------
# admin.py
#-----------------------------------------------------------------------

import flask
import database
import os 
import auth
import dotenv
import random
from flask import Flask, flash, redirect, url_for, request, render_template


#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------



@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    database.insert_player(username, 0)
    
    html_code = flask.render_template('index.html', username = username)
    # html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/requests', methods=['GET'])
def requests():
    pending_challenges = database.get_user_challenges(auth.authenticate())
    html_code = flask.render_template('this.html', challenges=pending_challenges)
    response = flask.make_response(html_code)
    return response

@app.route('/game', methods=['GET'])
def game():
    # get link from database
    # link = database.query()
    id = random.randint(1, 5)
    # coor = database.get_pic_info("coordinates", id)
    link = database.get_pic_info("link", id)

    # get user input using flask.request.args.get('')
    html_code = flask.render_template('gamepage.html', link = link, id = id)
    response = flask.make_response(html_code)
    # distance = flask.request.args.get('distance')
    # print('Distance: ' + distance)
    return response

#-----------------------------------------------------------------------

@app.route('/submit', methods=['POST'])
def submit():
    # get user input using flask.request.args.get('')
    #once user clicks submit then get coordinates 
    currLat = flask.request.form.get('currLat')  # Use .get for safe retrieval
    # print(currLat)
    currLon = flask.request.form.get('currLon')
    # print(currLon)
    # coor = database.get_distance()
    if not currLat or not currLon:
        return 
    
    id = flask.request.form.get('id')
    coor = database.get_pic_info("coordinates", id)
    # print(coor)

    distance = database.calc_distance(currLat, currLon, coor)
    username = auth.authenticate()

    points = database.calculate_points(username, distance)
    database.update_player(username, points)

    html_code = flask.render_template('results.html', dis = distance, lat = currLat, lon = currLon, coor=coor)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/rules', methods=['GET'])
def rules():
    html_code = flask.render_template('rules.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    top_players = database.get_top_players()
    html_code = flask.render_template('leaderboard.html', top_players = top_players)
    response = flask.make_response(html_code)
    return response

@app.route('/versus', methods=['GET'])
def versus():
    users = database.get_players()
    username = flask.request.args.get('username')
    html_code = flask.render_template('versus.html', users=flask.json.dumps(users), username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/create-challenge', methods=['POST'])
def create_challenge_route():
    challengee_id = flask.request.form['challengee_id'].strip()  # Trim whitespace
    users = database.get_players()  # Assuming this returns a list of usernames
    
    # Ensure challengee_id is not empty and exists in the users list
    if challengee_id == None or challengee_id not in users:
        response = {'status': 'error', 'message': 'Invalid challengee ID'}
        return flask.jsonify(response), 400  # Including a 400 Bad Request status code
    else:
        result = database.create_challenge(auth.authenticate(), challengee_id)
    
    # Handle the response from the database function
    if 'error' in result:
        return flask.jsonify({'status': 'error', 'message': result['error']}), 400  # Consider adding appropriate status codes
    else:
        return flask.jsonify({'status': 'success', 'message': result['success'], 'challenge_id': result['challenge_id']}), 200

@app.route('/accept_challenge', methods=['POST'])
def accept_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = database.accept_challenge(challenge_id)  # Assuming this returns some result
    if result == "accepted":
        flash('Challenge accepted successfully.')
    else:
        flash('Error accepting challenge.')
    return redirect(url_for('requests'))  # Assuming this is your route name

@app.route('/decline_challenge', methods=['POST'])
def decline_challenge_route():
    challenge_id = flask.request.form.get('challenge_id')
    result = database.decline_challenge(challenge_id)  # Assuming this returns some result
    if result == "declined":
        flash('Challenge declined successfully.')
    else:
        flash('Error declining challenge.')
    return redirect(url_for('requests'))

@app.route('/play_challenge', methods=['POST'])
def play_game():
    challenge_id = flask.request.form.get('challenge_id')
    html_code = flask.render_template('match.html', challenge_id=challenge_id)
    response = flask.make_response(html_code)
    return response

@app.route('/end_challenge', methods=['POST'])
def end_challenge():
    challenge_id = flask.request.form.get('challenge_id')
    database.complete_match(challenge_id, "ed8205", 10, 5)
    return redirect(url_for('index'))
    


