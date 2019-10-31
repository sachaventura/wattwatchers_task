from flask import Flask, request, Response

import wattwatchers_api.apiv3 as wattwatchers_api
import formatters
from utils import get_current_timestamp, joules_to_kwh

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
    from_ts = request.args.get('from_ts')
    to_ts = request.args.get('to_ts')
    granularity = request.args.get('granularity') or '30m'

    if wattwatchers_api.GRANULARITY.index(granularity) < wattwatchers_api.GRANULARITY.index('30m'):
        return 'Invalid granularity. Smallest granularity for monthly data is 30m', 400
    if from_ts and not from_ts.isdigit():
        return 'Invalid unix timestamp for from_ts.', 400
    if to_ts and not to_ts.isdigit():
        return 'Invalid unix timestamp for to_ts.', 400

    # compute timestamps to ensure we get 1 month worth of data
    # assume one month is 31 days for simplicity
    one_month_in_secs = 31 * 24 * 60 * 60
    if not from_ts and not to_ts:
        to_ts = get_current_timestamp()
        from_ts = to_ts - one_month_in_secs
    elif not to_ts:
        to_ts = int(from_ts) + one_month_in_secs
    elif not from_ts:
        from_ts = int(to_ts) - one_month_in_secs

    # make call to WattWatchers API
    try:
        results = wattwatchers_api.long_energy(api_key, device_id, granularity=granularity, from_ts=from_ts, to_ts=to_ts)
    except Exception as e:
        return 'Could not fetch data from wattwachers api: %s' % str(e), 400

    # convert energy values from joules to kWh
    for entry in results:
        for key in entry:
            if key in wattwatchers_api.ALL_ENERGY_FIELDS:
                entry[key] = [joules_to_kwh(int(x)) for x in entry[key]]

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