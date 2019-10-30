from flask import Flask, request, Response

import wattwatchers_api.apiv3 as wattwatchers_api
import formatters

app = Flask(__name__)

@app.route('/monthly_energy_csv')
def monthly_energy_csv():
    """Returns the WattWatchers long_energy endpoint formatted as csv

    params:
    - api_key: as specified by the WattWatchers API docs
    - device_id: as specified by the WattWatchers API docs
    - from_ts (optional)

    response:
    - status 200, with the csv in the body for successful requests
      Note: the units for the energy fields are kWh, unlike the WW API
    - status 400 for unsuccessful requests
    """

    # get parameters
    api_key = request.args.get('api_key')
    device_id = request.args.get('device_id')
    from_ts = request.args.get('from_ts') or None

    # make call to WattWatchers API
    try:
        results = wattwatchers_api.long_energy(api_key, device_id, from_ts)
    except:
        return 'Could not fetch data from wattwachers api', 400

     # determine the number of channels
    num_channels = 0
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
        num_channels = len(results[0].get(wattwatchers_api.LONG_ENERGY_DATA_FIELDS[0], []))

    csv = formatters.to_csv(results,
        header_fields=wattwatchers_api.HEADER_FIELDS,
        data_fields=wattwatchers_api.LONG_ENERGY_DATA_FIELDS,
        num_channels=num_channels)

    return Response(csv, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')