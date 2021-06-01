# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Getting Started 

## Frontend
> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Backend
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, and the frontend app runs locally at, http://127.0.0.1:3000/

- Authentication: This version of the application does not require authentication or API keys.

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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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

## Error Handling
```
{
    "success": False,
    "error": 404,
    "message": "Resource not found"
}
```
- The API will return three error types when requests fail:
    - 400: Bad Request
    - 404: Resource Not Found
    - 405: Method Not Allowed
    - 422: Not Processable
    - 500: Internal Server Error

## Endpoints
### GET /categories
- description:
    - returns a json of categories and sucess
    - example using postman
GET ```http://127.0.0.1:5000/categories```
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
### GET /questions
- description:
    - returns a json of categories, list of paginated questions, total number of questions in the database, and success value
    - example using postman
GET ```http://127.0.0.1:5000/questions?page=2```
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 35,
            "question": "test"
        }
    ],
    "success": true,
    "total_questions": 18
}
```
### DELETE /questions/{id}
- description:
    - deletes the question of given id from database if it's found
    - returns success value and id of deleted question
- example using postman
DELETE ```http://127.0.0.1:5000/questions/5```
```
{
    "id": 5,
    "success": true
}
```
### POST /questions
- description:
    - adds new question to database
    - returns success value and a message
- example using postman
POST ```http://127.0.0.1:5000/questions```
```
json body = {
    "question":"test question?",
    "answer":"test answer",
    "difficulty": 1,
    "category": 1
}
```
```
{
    "message": "question added",
    "success": true
}

```

### POST /questions/search
- description:
    - searchs for questions in the database
    - returns success value, a list of questions and the total number of found questions
- example using postman
POST ```http://127.0.0.1:5000/questions/search```
```
json body = {
    "searchTerm":"test"
}
```
```
{
    "questions": [
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 35,
            "question": "test"
        },
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 36,
            "question": "test"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

### GET /categories/{id}/questions
- description:
    - gets questions of a specific category given its id
    - returns success value, a list of questions, the total number questions of this category and category id
- example using postman
GET ```http://127.0.0.1:5000/categories/1/questions```
```
{
    "current_category": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 35,
            "question": "test"
        },
        {
            "answer": "test",
            "category": 1,
            "difficulty": 1,
            "id": 36,
            "question": "test"
        }
    ],
    "success": true,
    "total_questions": 5
}
```


### POST /quizzes
- description:
    - sends a list of question ids, and category id and type in a json body
    - returns success value, and a new question that is not in the previous questions list
- example using postman
POST ```http://127.0.0.1:5000/quizzes```
```
json body = {

    "previous_questions":[],
    "quiz_category": {
        "type": "Science",
        "id": 1
    }
}
```
```
{
    "question": {
        "answer": "test",
        "category": 1,
        "difficulty": 1,
        "id": 36,
        "question": "test"
    },
    "success": true
}
```

## Test
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


## Authors
- Amr Ehab