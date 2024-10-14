from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def load_event_data():
    with open('eventData.json', 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)
    return data

@app.route('/')
def index():
    events = load_event_data()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
