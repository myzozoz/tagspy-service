# Entry point
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.service import analyze_reviews, fetch_tags

app = Flask(__name__)
CORS(app)

@app.route('/')
def greet():
  return '<p>Hello and welcome. Please call a specific API.</p>'

@app.route('/api/')
def api_greet():
    return {'message': 'Please call a specific API'}

@app.route('/api/summary')
def summary():
  tags = request.args.get('tags',['']).split(',')
  print(tags)
  response_data = analyze_reviews(tags)
  return jsonify(response_data)

@app.route('/api/tags')
def tags():
  return jsonify(fetch_tags())