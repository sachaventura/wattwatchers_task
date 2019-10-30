import unittest

from app import app

class MonthlyEnergyTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_valid_credentials(self):
        response = self.app.get('/monthly_energy_csv?api_key=key_4179959b76294b92a26eab1c47cc3f36&device_id=D704206228658')
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials(self):
        response = self.app.get('/monthly_energy_csv?api_key=key_foobar&device_id=D704206228658')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()