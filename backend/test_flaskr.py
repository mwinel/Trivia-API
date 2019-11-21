import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:123456@{}/{}".format(
            'localhost:5432', self.database_name)
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

    def test_get_categories(self):
        """Test get categories."""
        res = self.client.get("/categories")
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_questions(self):
        """Test get questions."""
        res = self.client.get("/questions?page=1")
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question(self):
        """Test delete a question given its id."""
        res = json.loads(self.client.get("/questions").data.decode())
        count_one = res['total_questions']
        res = self.client.delete(
            f'/questions/{random.choice(res["questions"])["id"]}')
        count_two = json.loads(self.client.get(
            "/questions").data.decode())['total_questions']
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(count_one, count_two + 1)
        self.assertEqual(result["success"], True)
        self.assertEqual(result["message"], "Question successfully deleted.")

    def test_post_question(self):
        """Test creating a new question."""
        body = {
            "question": "What is my name?",
            "answer": "Nelson Mwiru",
            "category": 6,
            "difficulty": 3
        }
        count_one = json.loads(self.client.get(
            "/questions").data.decode())["total_questions"]
        res = self.client.post("/questions",
                               content_type="application/json",
                               data=json.dumps(body))
        count_two = json.loads(self.client.get(
            "/questions").data.decode())["total_questions"]
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(count_one, count_two - 1)
        self.assertEqual(result["success"], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
