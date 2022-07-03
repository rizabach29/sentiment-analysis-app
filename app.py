import json
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

@app.route('/crawling-data/<string:ecommerce>', methods=['GET'])
def crawling_data_ecommerce(ecommerce):
    # ecommerceParam = request.args.get("ecommerce", None)
    if ecommerce != "shopee" and ecommerce != "lazada" and ecommerce != "tokopedia" and ecommerce != "bukalapak" and ecommerce != "blibli":
        return {'message': 'ecommerce parameter invalid!'}, 400

    # crawling data by ecommerce
    crawled_data = [
        {'tweetId': '1', 'username': '@User1', 'tweet': 'Ini tweet hasil crawling dari @User1 '+ecommerce},
        {'tweetId': '2', 'username': '@User2', 'tweet': 'Ini tweet hasil crawling dari @User2 '+ecommerce},
        {'tweetId': '3', 'username': '@User3', 'tweet': 'Ini tweet hasil crawling dari @User3 '+ecommerce}
    ]

    return jsonify(crawled_data)

@app.route('/analyze-tweets', methods=['POST']) #request body array of object: string tweet, username, datetime
def analyze_tweet():
    # parser = reqparse.RequestParser()
    # args = parser.parse_args()
    record = json.loads(request.data)

    if not(isinstance(record, list)):
        return {'message': 'Request body must be in array formed !'}, 400
    if len(record) <= 0:
        return {'message': 'Request body array must not be empty !'}, 400

    sentimented = [
        {'tweetId': '1', 'sentiment': 'Negative'},
        {'tweetId': '2', 'sentiment': 'Netral'},
        {'tweetId': '3', 'sentiment': 'Positive'}
    ]
    responses = {
        "data": sentimented
    }
    return jsonify(responses) #return array of object string hasil sentiment analysis

@app.route('/count-sentiment', methods=['POST']) #request body array of string/int sentiment analysis
def count_percentage():
    record = json.loads(request.data)

    if not(isinstance(record, list)):
        return {'message': 'Request body must be in array formed !'}, 400
    if len(record) <= 0:
        return {'message': 'Request body array must not be empty !'}, 400

    percentage = [
        {'Negative': 140},
        {'Netral': 220},
        {'Positive': 310}
    ]
    responses = {
        "data": percentage
    }

    return jsonify(responses) #return array of int percentage: positif, negatif, netral

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)