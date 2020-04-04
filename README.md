# Full Stack Trivia

## Getting Started

Project is divided into `frontend` and `backend` directory.

Technologies used in the project:
**Frontend**

- React
- React Router
- Jquery

**Backend**

- Flask
- SQLAlchemy
- Flask CORS

**Database**

- PostgresSQL

## Installation

**Frontend**

```bash
cd frontend/
# Installing dependencies
npm install
# Starting the project
npm run start
```

**Backend**
Creating db and populating data.

**_NOTE: Make sure postgres in running_**

```bash
# Creating db
createdb trivia

cd backend/

# Populating database with tables and related data
psql trivia < trivia.psql
```

```bash
# Creating virtual environment
virtualenv venv

# Activating virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Start your project in development mode
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## API Documentation

**_API follows Restful API convenctions._**

The main data returned for both success and failed responses are in the `data` object. For failed response data contains the message of why it failed and for successfull response data is the main thing requested by the client. Although, other supporting data will be contained in the successful response.

```JSON
{
    "success": true/false,
    "data": "main data here",
    ...
}
```

### Endpoints

**/categories** [GET]

Sample Response:

```JSON
{
  "data": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total": 6
}
```

---

**/questions?page=1** [GET]

_NOTE: Only 10 questions are returned per page_

Sample Response:

```JSON
{
  "category": "All",
  "data": {
    "categories": [
      {
        "id": 1,
        "type": "Science"
      },
      ...
    ],
    "questions": [
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      },
      ...
    ],
  "success": true,
  "total": 31
}
```

**/questions/\<int:question_id\>** Request Type: [DELETE]

Sample Response:

```JSON
{
  "success": true
}
```

---

**/questions** Request Type: [POST]

Data: `{"search": "won"}`

Sample Response:

```JSON
{
  "success": true,
  "data": [
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
  ],
  "total": 1
}
```

---

**/category/\<int:category_id\>/questions** Request Type: [GET]

Sample Response:

```JSON
{
  "category": 1,
  "data": [
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
    }
  ],
  "success": true,
  "total": 2
}
```

---

**/quiz/question** Request Type: [POST]

Data: `{"category": 1, "previous_questions": [23]}`

Sample Response:

```json
{
  "data": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```
