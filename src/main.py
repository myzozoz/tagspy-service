# Entry point
from flask import Flask, request, jsonify
import service

app = Flask(__name__)

@app.route('/')
def greet():
  return '<p>Hello and welcome. Please call a specific API.</p>'

@app.route('/api/')
def api_greet():
    return {'message': 'Please call a specific API'}

@app.route('/api/games')
def games():
  tags = request.args.get('tags',['']).split(',')
  print(tags)
  response_data = service.analyze_reviews(tags)
  return jsonify(response_data)