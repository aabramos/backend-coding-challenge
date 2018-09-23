# Unbabel Backend Challenge

## Challenge

1) Build a basic web app with a simple input field that takes an English (EN) input translates it to Spanish (ES).
2) When a new translation is requested it should add to a list below the input field (showing one of three status: requested, pending or translated) - (note: always request human translation)
3) The list should be dynamically ordered by the size of the translated messages

#### Requirements
* Use Flask web framework
* Use PostgreSQL
* Create a scalable application. 
* Only use Unbabel's Translation API on sandbox mode
* Have tests

#### Notes
* Page load time shouldnt exceed 1 second

#### TODO's
1. Set up infrastructure **[OK]**
2. Development of forms.py **[OK]**
3. Development of models.py **[OK]**
4. Implementing of database migrations **[OK]**
5. Development of views.py **[OK]**
6. Unit tests **[OK]**
7. Real time table **[OK]**
8. Documentation **[OK]**

####  Resources
* Unbabel's API: http://developers.unbabel.com/

##  Instalation:

1) Clone the repository:
```
git clone https://github.com/aabramos/backend-coding-challenge
cd backend-coding-challenge
```
2) Install dependencies:

[- PostgreSQL](https://www.postgresql.org/);

[- Redis](http://redis.io/).

And create a database on PostgreSQL. 

3) Run install.sh (or install.cmd if using Windows):
```
./install.sh
```
4) Initialize database:
```
flask db migrate
flask db upgrade
```
5) Create a environment`.env` file using the following syntax:

```
SECRET_KEY=YourSecretKey
SANDBOX_USERNAME=YourUnbabelAPISandboxUsername
SANDBOX_KEY=YourUnbabelAPISandboxKey
POSTGRES_USER=YourPostgresUser
POSTGRES_PW=YourPostgresConfiguration
POSTGRES_DB=YourPostgresConfiguration
POSTGRES_HOST=YourPostgresConfiguration
POSTGRES_PORT=YourPostgresConfiguration
POSTGRES_USER_TEST=YourPostgresTestConfiguration
POSTGRES_PW_TEST=YourPostgresTestConfiguration
POSTGRES_DB_TEST=YourPostgresTestConfiguration
POSTGRES_HOST_TEST=YourPostgresTestConfiguration
POSTGRES_PORT_TEST=YourPostgresTestConfiguration
```
6) Run Celery:
```
celery -A app.tasks worker -B --loglevel=info
```
7) Open another terminal to run the application:
```
./run.sh
```
And access http://localhost:5000 on your browser.

### Approach
- After a translation request is made by submitting the text on the frontend, an Unbabel-py API request is made in the backend, sending a human translation request to The Unbabel server.

- Note:The folder /Unbabel contains a local customized Unbabel-py API. The original wasn't compatible with Python 3.6. Check out [my fork](https://github.com/aabramos/unbabel-py);

- All requests are made using a job queue, with Celery as the background processor and Redis as the broker.

- The first request saves the translation in the database, and the subsequent jobs ask the status of the translation with Unbabel server every 30 seconds, updating the information on the database if necessary;

- The comunication between the frontend and the backend are made with Socket.io, updating the table below the submit field without refreshing the page and sorting the list using the translated messages length.

### Testing
Commands:
```
python -m unittest app.test.test_set_up
python -m unittest app.test.test_celery
python -m unittest app.test.test_unbabel
```
Notes:
- test_set_up: Tests if the app and the SQLAlchemy is working correctely. This test will also send db commands like drop_all() to your test database, so migrate and upgrade the test database after this test if needed;
- test_celery: test if celery/redis is working correctely. Run celery in another terminal for this test;
- test_unbabel: make a test request to unbabel, validating the response data.
