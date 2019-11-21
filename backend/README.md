# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## REST API specifications

The REST API is described below.

## GET questions

### Request

```
GET /questions
postman 'Accept: application/json' http://127.0.0.1:5000/questions?page=2
- request args: None
```

### Response

```
HTTP/1.1 200 OK
Date: Thu, 21 Nov 2019 12:36:30 GMT
Status: 200 OK
Connection: close
Content-Type: application/json
Content-Length: 2

{
    "next_url": /questions?page=3,
    "prev_url": "/questions?page=1",
    "questions": [
        {
            "answer": "Agra",
            "category": "Geography",
            "category_id": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Mona Lisa",
            "category": "Art",
            "category_id": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        ...
    ],
    "success": true,
    "total_questions": 1990
}
```

## GET categories

### Request

```
GET /categories
postman 'Accept: application/json' http://127.0.0.1:5000/categories
- request args: None
```

### Response

```
HTTP/1.1 200 OK
Date: Thu, 21 Nov 2019 12:36:30 GMT
Status: 200 OK
Connection: close
Content-Type: application/json
Content-Length: 2

{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "success": true
}
```

## POST question

### Request

```
POST /questions
postman 'Accept: application/json' http://127.0.0.1:5000/questions
- request args: None

{
	"question": "Who directed the movie 'Once Upon a time in Hollywood'?",
	"answer": "Quentin Tarantino",
	"category": 4,
	"difficulty": 2
}
```

### Response

```
HTTP/1.1 201 Created
Date: Thu, 21 Nov 2019 12:36:30 GMT
Status: 201 Created
Connection: close
Content-Type: application/json
Content-Length: 2

{
    "message": "Question successfully created.",
    "question": {
        "answer": "Quentin Tarantino",
        "category": 4,
        "difficulty": 2,
        "id": 24,
        "question": "Who directed the movie 'Once Upon a time in Hollywood'?"
    },
    "success": true
}
```

## DELETE question

### Request

```
DELETE /questions/<question_id>
postman 'Accept: application/json' http://127.0.0.1:5000/questions/25
- request args: <question_id>
```

### Response

```
HTTP/1.1 200 OK
Date: Thu, 21 Nov 2019 12:36:30 GMT
Status: 200 OK
Connection: close
Content-Type: application/json
Content-Length: 2

If True:

{
    "message": "Question successfully deleted."
    "success": true
}

else:

{
    "message": "Question not found."
    "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
