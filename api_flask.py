import time, datetime, hashlib, json, requests

from flask import Flask, request

# your API key and secret
apiKey = "2wdqtq7jzv7m8jzuemuufns5"
sharedSecret = "NRm6Eb5G7n"

# endpoints
hb_activities_url = "https://api.test.hotelbeds.com/activity-api/3.0/activities"

app = Flask(__name__)


@app.route("/get_today_activities", methods=['GET'])
def today_activities():
    ## yyyy-mm-dd format
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    today = today.strftime("%Y-%m-%d")
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    city = request.args.get("city")
    age = request.args.get("age")

    # get signature
    sigStr = "%s%s%d" % (apiKey, sharedSecret, int(time.time()))
    signature = hashlib.sha256(sigStr.encode()).hexdigest()

    # create http request and add headers
    headers = {}
    headers['X-Signature'] = signature
    headers['Api-Key'] = apiKey
    headers['Accept'] = "application/json"
    headers['Content-Type'] = "application/json"

    responses = {}
    for i in range(1, 5):
        body = json.dumps({"filters": [{"searchFilterItems": [{"type": "destination", "value": city},
                                                   {"type": "segment", "value": str(i)},
                                                   {"type": "segment", "value": age}]}],
                "from": today, "to": tomorrow, "language": "en",
                "pagination": {"itemsPerPage": 1, "page": 1}, "order": "PRICE"})
        r = requests.post(url=hb_activities_url, headers=headers, data=body)
        responses[i] = r.text
    return json.dumps(responses)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
