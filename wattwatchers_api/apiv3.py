import requests
import json

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

def joules_to_kwh(joules):
    return  joules / 3600000

def make_get_request(uri, **kwargs):
    return requests.get('%s/%s' % (WATTWATCHERS_API_V3_URL, uri), **kwargs)

def long_energy(api_key, device_id, granularity = '5m', fromTs = None):
    headers = {
        'Authorization': 'Bearer {0}'.format(api_key)
    }
    params = {
        'granularity': granularity
    }

    if fromTs:
        params['fromTs'] = fromTs

    uri = 'long-energy/{device_id}'.format(device_id=device_id)

    response = make_get_request(uri, headers=headers, params=params)

    if (response.status_code != 200):
        raise Exception(response.text)
    # handle request error

    results = json.loads(response.content)

    for entry in results:
        for key in entry:
            if key in ALL_ENERGY_FIELDS:
                entry[key] = [joules_to_kwh(int(x)) for x in entry[key]]

    return results