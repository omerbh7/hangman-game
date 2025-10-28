from flask import Flask, render_template, request, session, jsonify
import requests
import string
import random
from flask import redirect, url_for
from flask_session import Session

API_URL = "https://random-word-api.herokuapp.com/word"

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

MAX_ATTEMPTS = 6


def get_random_word():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0].lower()
        else:
            return "python"
    except Exception:
        return "python"


def start_new_game():
    word = get_random_word()
    session['word'] = word
    session['guessed_letters'] = []
    session['wrong_guesses'] = []
    session['max_attempts'] = MAX_ATTEMPTS
    session['game_over'] = False
    session['won'] = False


def get_display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])


@app.route("/")
def index():
    if 'word' not in session or session.get('game_over', False):
        start_new_game()
    word = session['word']
    guessed_letters = session['guessed_letters']
    wrong_guesses = session['wrong_guesses']
    display_word = get_display_word(word, guessed_letters)
    return render_template("index.html", display_word=display_word, wrong_guesses=wrong_guesses, max_attempts=MAX_ATTEMPTS, game_over=session['game_over'], won=session['won'], word=word)


@app.route("/guess", methods=["POST"])
def guess():
    if session.get('game_over', False):
        return jsonify({'error': 'Game is over.'}), 400
    letter = request.form.get('letter', '').lower()
    word = session['word']
    guessed_letters = session['guessed_letters']
    wrong_guesses = session['wrong_guesses']
    if not letter or len(letter) != 1 or letter not in string.ascii_lowercase:
        return jsonify({'error': 'Invalid input.'}), 400
    if letter in guessed_letters or letter in wrong_guesses:
        return jsonify({'error': 'Already guessed.'}), 400
    if letter in word:
        guessed_letters.append(letter)
        if all(l in guessed_letters for l in word):
            session['game_over'] = True
            session['won'] = True
    else:
        wrong_guesses.append(letter)
        if len(wrong_guesses) >= MAX_ATTEMPTS:
            session['game_over'] = True
            session['won'] = False
    session['guessed_letters'] = guessed_letters
    session['wrong_guesses'] = wrong_guesses
    return jsonify({
        'display_word': get_display_word(word, guessed_letters),
        'wrong_guesses': wrong_guesses,
        'game_over': session['game_over'],
        'won': session['won'],
        'word': word if session['game_over'] else None
    })


@app.route("/restart", methods=["POST"])
def restart():
    start_new_game()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
