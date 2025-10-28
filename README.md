# Hangman Game with Random Word API (Web & Docker)

This is a web-based Hangman game in Python using Flask. Each game fetches a new random word using the free Random Word API:

https://random-word-api.herokuapp.com/word

## How to run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open your browser at http://localhost:5000

## How to run with Docker

1. Build the Docker image:

```bash
docker build -t hangman-game .
```

2. Run the container:

```bash
docker run -p 5000:5000 hangman-game
```

3. Open your browser at http://localhost:5000

## API Info
- The game uses the endpoint: `https://random-word-api.herokuapp.com/word` to get a random word.
- No API key or signup required.

## Project structure
- `app.py` — Flask backend
- `templates/index.html` — Main HTML UI
- `static/css/style.css` — CSS for the UI
- `Dockerfile`, `.dockerignore` — For containerization
- `requirements.txt` — Python dependencies
