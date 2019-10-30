from flask import Flask, request, Response
import requests

app = Flask(__name__)

def fetch_data(api_key, device_id):
    headers = {
        'Authorization': 'Bearer %s' % api_key
    }
    params={
        'granularity': '30m'
    }
    response = requests.get('https://api-v3.wattwatchers.com.au//long-energy/%s' % device_id, headers=headers, params=params)
    return response.content

@app.route('/monthly_energy')
def monthly_energy():
    api_key = request.args.get('api_key')
    device_id = request.args.get('device_id')
    data = fetch_data(api_key, device_id)
    return Response(data, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')