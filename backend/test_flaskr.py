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
        # self.assertTrue(isinstance(res["categories"], list))

    # def test_get_questions(self):
    #     """Test get questions."""
    #     res = self.client.get("/questions")
    #     data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code, 200)
        # self.assertTrue()(isinstance(res["questions"], list))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
