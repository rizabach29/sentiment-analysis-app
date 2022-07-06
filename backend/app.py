import json
from flask import Flask, jsonify, request, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from ansimeter_v2 import crawlingTweet, preprocessing1, preprocessing2, postagging, scoring, label_sentiment

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/crawling-data/<string:ecommerce>', methods=['GET'])
def crawling_data_ecommerce(ecommerce):
    # ecommerceParam = request.args.get("ecommerce", None)
    if ecommerce != "shopee" and ecommerce != "lazada" and ecommerce != "tokopedia" and ecommerce != "bukalapak" and ecommerce != "blibli":
        return {'message': 'ecommerce parameter invalid!'}, 400

    shopeeArray = ['ShopeeID','shopee','shopeecare','syopi']
    lazadaArray = ['lazada','LazadaCare','LazadaID']
    tokopediaArray = ['tokopedia','tokopediacare','tokped']
    bukalapakArray = ['BukaBantuan','bukalapak']
    blibliArray = ['blibli','bliblicare','bliblidotcom']

    results = []
    dataEcommerce = []
    if ecommerce == "shopee":
        dataEcommerce = shopeeArray
    elif ecommerce == "lazada":
        dataEcommerce = lazadaArray
    elif ecommerce == "tokopedia":
        dataEcommerce = tokopediaArray
    elif ecommerce == "bukalapak":
        dataEcommerce = bukalapakArray
    elif ecommerce == "blibli":
        dataEcommerce = blibliArray

    for dat in dataEcommerce:
        res = crawlingTweet(dat)
        for val in res:
            # if isinstance(val, bytes):
            #     results.append(val)
            #     continue
            results.append(val)

    # print("HASIL: ", results[0])
    return json.dumps(results, indent=4, sort_keys=True, default=str)

@app.route('/analyze-tweets', methods=['POST']) #request body array of object: string tweet, username, datetime
def analyze_tweet():
    # parser = reqparse.RequestParser()
    # args = parser.parse_args()
    records = json.loads(request.data)

    if not(isinstance(records, list)):
        return {'message': 'Request body must be in array formed !'}, 400
    if len(records) <= 0:
        return {'message': 'Request body array must not be empty !'}, 400
    # print("TYPE: ", type(records[0])) #array of dict

    resultTemps = []
    for record in records:
        resTemp = preprocessing1(record['tweet'])
        tokenizedTemp = preprocessing2(resTemp)
        postaggedTemp = postagging(tokenizedTemp)
        resultTemps.append(postaggedTemp)

    scoredText = scoring(resultTemps)
    labeledText = label_sentiment(scoredText)

    results = []
    for idx, record in enumerate(records):
        results.append({'date': record['date'], 'username': record['username'], 'tweet': record['tweet'], 'sentiment': labeledText[idx]})

    responses = {
        "data": results
    }
    return jsonify(responses) #return array of object string hasil sentiment analysis

@app.route('/count-sentiment', methods=['POST']) #request body array of string/int sentiment analysis
def count_percentage():
    records = json.loads(request.data)

    if not(isinstance(records, list)):
        return {'message': 'Request body must be in array formed !'}, 400
    if len(records) <= 0:
        return {'message': 'Request body array must not be empty !'}, 400

    negativeArr = []
    positiveArr = []
    netralArr = []
    for idx, val in enumerate(records):
        if 'sentiment' in val:
            if (val['sentiment'] == 'Negative') or (val['sentiment'] == 'negative'):
                negativeArr.append(val['sentiment'])
            elif (val['sentiment'] == 'Positive') or (val['sentiment'] == 'positive'):
                positiveArr.append(val['sentiment'])
            elif (val['sentiment'] == 'Netral') or (val['sentiment'] == 'netral'):
                netralArr.append(val['sentiment'])

    percentage = [
        {'Negative': len(negativeArr)},
        {'Netral': len(netralArr)},
        {'Positive': len(positiveArr)}
    ]
    responses = {
        "data": percentage
    }

    return jsonify(responses) #return array of int percentage: positif, negatif, netral

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)