import requests
import json

from utils import joules_to_kwh

WATTWATCHERS_API_V3_URL = 'https://api-v3.wattwatchers.com.au'

DURATION_FIELD = 'duration'
TIMESTAMP_FIELD = 'timestamp'
REAL_ENERGY_FIELDS = ['eReal', 'eRealPositive', 'eRealNegative']
REACTIVE_ENERGY_FIELDS = ['eReactive', 'eReactivePositive', 'eReactiveNegative']
VOLTAGE_FIELDS = ['vRMSMin', 'vRMSMax']
CURRENT_FIELDS = ['iRMSMin', 'iRMSMax']
ALL_ENERGY_FIELDS = REAL_ENERGY_FIELDS + REACTIVE_ENERGY_FIELDS
HEADER_FIELDS = [DURATION_FIELD, TIMESTAMP_FIELD]
LONG_ENERGY_DATA_FIELDS = ALL_ENERGY_FIELDS + VOLTAGE_FIELDS + CURRENT_FIELDS

def make_get_request(path, api_key, **kwargs):
    kwargs['headers'] = {
        **kwargs.get('headers', {}),
        'Authorization': 'Bearer {0}'.format(api_key)
    }
    endpoint = '{url}/{path}'.format(url=WATTWATCHERS_API_V3_URL, path=path)
    return requests.get(endpoint, **kwargs)

def long_energy(api_key, device_id, granularity = None, from_ts = None):
    params = {}

    if granularity:
        params['granularity'] = granularity

    if from_ts:
        params['fromTs'] = from_ts

    path = 'long-energy/{device_id}'.format(device_id=device_id)

    response = make_get_request(path, api_key=api_key, params=params)

    if (response.status_code != 200):
        raise Exception(response.text)

    # parse JSON
    results = json.loads(response.content)

    # convert energy values from joules to kWh
    for entry in results:
        for key in entry:
            if key in ALL_ENERGY_FIELDS:
                entry[key] = [joules_to_kwh(int(x)) for x in entry[key]]

    return results