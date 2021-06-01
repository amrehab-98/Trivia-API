import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_NAME)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_200(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions_200(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], len(Question.query.all()))
        self.assertEqual(len(data['categories']), 6)

    def test_get_paginated_questions_404(self):
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question_200(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 5)

    def test_delete_question_404(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_question_200(self):
        res = self.client().post('/questions', json={
            "question": "test question",
            "answer": "test answer",
            "difficulty": 2,
            "category": 1
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'question added')

    def test_add_empty_question_400(self):
        res = self.client().post('/questions', json={
            "question": "",
            "answer": "test answer",
            "difficulty": 2,
            "category": 1
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_add_missing_answer_400(self):
        res = self.client().post('/questions', json={
            "question": "test question",
            "difficulty": 2,
            "category": 1
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_search_200(self):
        searchTerm = "world cup"
        res = self.client().post('/questions/search', json={
            "searchTerm": "world cup"
            })
        data = json.loads(res.data)
        search = Question.query.filter(
            Question.question.ilike(f"%{searchTerm}%")).all()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(search))
        self.assertTrue(data['questions'])

    def test_search_with_no_body_400(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    def test_get_questions_by_category_200(self):
        questions = Question.query.filter_by(category=1).all()

        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(questions))
        self.assertTrue(data['questions'])

    def test_get_questions_by_category_404(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Resource Not Found")
        self.assertEqual(data['success'], False)

    def test_get_quizzes_200(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {
                "type": "Science",
                "id": 1
            }
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_quizzes_no_id_400(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {
                "type": "Science",
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
