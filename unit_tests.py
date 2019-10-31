import unittest

from app import app
import wattwatchers_api.apiv3 as wattwatchers_api

VALID_API_KEY = 'key_4179959b76294b92a26eab1c47cc3f36'
VALID_DEVICE_ID = 'D704206228658'
INVALID_API_KEY = 'foobar'
INVALID_DEVICE_ID = 'marmaduke'

# High-level Flask API test
class MonthlyEnergyTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_valid_credentials(self):
        response = self.app.get('/monthly_energy_csv?api_key={api_key}&device_id={device_id}'.format(api_key=VALID_API_KEY, device_id=VALID_DEVICE_ID))
        self.assertEqual(response.status_code, 200)

    def test_invalid_from_ts(self):
        response = self.app.get('/monthly_energy_csv?api_key={api_key}&device_id={device_id}&from_ts=foobar'.format(api_key=VALID_API_KEY, device_id=VALID_DEVICE_ID))
        self.assertEqual(response.status_code, 400)

    def test_invalid_credentials(self):
        response = self.app.get('/monthly_energy_csv?api_key={api_key}&device_id={device_id}'.format(api_key=INVALID_API_KEY, device_id=VALID_DEVICE_ID))
        self.assertEqual(response.status_code, 400)

# Low-level wattwatchers API wrapper test
class WattWatcherAPITests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_valid(self):
        result = wattwatchers_api.long_energy(api_key=VALID_API_KEY, device_id=VALID_DEVICE_ID)
        self.assertEqual(isinstance(result, list), True)
        self.assertGreater(len(result), 0)

    def test_granularity(self):
        for granularity in [5, 15]:
            result = wattwatchers_api.long_energy(api_key=VALID_API_KEY, device_id=VALID_DEVICE_ID, granularity='{0}m'.format(granularity))
            self.assertEqual(result[0]['duration'], granularity * 60) # duration is in seconds

    def test_from_ts(self):
        for from_ts in [1546261200 + 3600, 1546261200 + 7200]:
            result = wattwatchers_api.long_energy(api_key=VALID_API_KEY, device_id=VALID_DEVICE_ID, from_ts=from_ts)
            self.assertEqual(result[0]['timestamp'], from_ts)

    def test_invalid_credentials(self):
        with self.assertRaises(Exception):
            wattwatchers_api.long_energy(api_key=INVALID_API_KEY, device_id=VALID_DEVICE_ID)

    def test_invalid_device_id(self):
        with self.assertRaises(Exception):
            wattwatchers_api.long_energy(api_key=VALID_API_KEY, device_id=INVALID_DEVICE_ID)


if __name__ == "__main__":
    unittest.main()