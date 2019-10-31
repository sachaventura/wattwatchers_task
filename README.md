# WattWatchers Technical Appraisal task - Sacha Ventura
Flask API that wraps around the WattWatchers' API.
Currently the only endpoint implemented is:

`GET /monthly_energy_csv`

Request parameters:

| parameter     | format        | required | Notes |
| ------------- |:-------------:| --------:| -----:|
| api_key       | string        |        Y |       |
| device_id     | string        |        Y |       |
| from_ts       | integer       |        N | Unix timestamp, seconds since epoch. Returns data with timestamp >= fromTs. Default, if not specified: first long energy entry.|

## Build & Run
Docker is used to containerise the Python + Flask application.

Build the docker image:

`docker build -t wattwatchers-task:latest .`

Run the image:

`docker run -p 5000:5000 wattwatchers-task`

See the results by opening the following URL in your browser:
http://0.0.0.0:5000/monthly_energy_csv?api_key=key_4179959b76294b92a26eab1c47cc3f36&device_id=D704206228658

# Unit tests
The tests are run automatically during the docker image build process.


# Structure
I have opted for the most pragmatic "Single Module" structure, considering the project size and to save time with the project setup:

`This is great for quick projects (like the ones used for tutorials), where you just need to serve a few routes and you’ve got less than a few hundred lines of application code.`

http://exploreflask.com/en/latest/organizing.html#single-module